import json
from functools import wraps
from flask import request, Blueprint, render_template, jsonify, flash, \
    redirect, url_for, abort
from flask_restful import Resource, reqparse
from my_app import db, app, api
from my_app.catalog.models import Product, Category
from sqlalchemy.orm import join 

catalog = Blueprint('catalog', __name__)


def template_or_json(template=None):
    """"Return a dict from your view and this will either
    pass it to a template or render json. Use like:

    @template_or_json('template.html')
    """
    def decorated(f):
        @wraps(f)
        def decorated_fn(*args, **kwargs):
            ctx = f(*args, **kwargs)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or not template:
                return jsonify(ctx)
            else:
                return render_template(template, **ctx)
        return decorated_fn
    return decorated


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@catalog.route('/')
@catalog.route('/home')
@template_or_json('home.html')
def home():
    products = Product.query.all()
    return {'count': len(products)}


@catalog.route('/product/<id>')
def product(id):
    product = Product.query.get_or_404(id)
    return render_template('product.html', product=product)


@catalog.route('/products')
@catalog.route('/products/<int:page>')
def products(page=1):
    products = Product.query.paginate(page=page, per_page=10, error_out=False)
    return render_template('products.html', products=products)


@catalog.route('/product-create', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        categ_name = request.form.get('category')
        category = Category.query.filter_by(name=categ_name).first()
        if not category:
            category = Category(categ_name)
        product = Product(name, price, category)
        db.session.add(product)
        db.session.commit()
        flash('The product %s has been created' % name, 'success')
        return redirect(url_for('catalog.product', id=product.id))
    return render_template('product-create.html')


@catalog.route('/product-search')
@catalog.route('/product-search/<int:page>')
def product_search(page=1):
    name = request.args.get('name')
    price = request.args.get('price')
    company = request.args.get('company')
    category = request.args.get('category')
    products = Product.query
    if name:
        products = products.filter(Product.name.like('%' + name + '%'))
    if price:
        products = products.filter(Product.price == price)
    if company:
        products = products.filter(Product.company.like('%' + company + '%'))
    if category:
        products = products.select_from(join(Product, Category)).filter(
            Category.name.like('%' + category + '%')
        )
    return render_template(
        'products.html', products=products.paginate(page, 10)
    )


@catalog.route('/category-create', methods=['POST',])
def create_category():
    name = request.form.get('name')
    category = Category(name)
    db.session.add(category)
    db.session.commit()
    return render_template('category.html', category=category)


@catalog.route('/category/<id>')
def category(id):
    category = Category.query.get_or_404(id)
    return render_template('category.html', category=category)


@catalog.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)


parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('price', type=float)
parser.add_argument('category', type=dict)


class ProductApi(Resource):

    def get(self, id=None, page=1):
        if not id:
            products = Product.query.paginate(page=page, per_page=10, error_out=False).items
        else:
            products = [Product.query.get(id)]
        if not products or products == [None]:
            abort(404, description="Products not found")
        
        res = {
            product.id: {
                'name': product.name,
                'price': product.price,
                'category': product.category.name
            } for product in products
        }
        return jsonify(res)

    def post(self):
        data = request.get_json()
        if not data or 'name' not in data or 'price' not in data or 'category' not in data:
            abort(400, description="Missing required fields")
        
        name = data['name']
        price = data['price']
        category_name = data['category']

        category = Category.query.filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            db.session.add(category)

        product = Product(name=name, price=price, category=category)
        db.session.add(product)
        db.session.commit()

        res = {
            product.id: {
                'name': product.name,
                'price': product.price,
                'category': product.category.name
            }
        }
        return jsonify(res), 201

    def put(self, id):
        data = request.get_json()
        if not data or 'name' not in data or 'price' not in data or 'category' not in data:
            abort(400, description="Missing required fields")
        
        name = data['name']
        price = data['price']
        category_name = data['category']

        category = Category.query.filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            db.session.add(category)

        product = Product.query.get_or_404(id)
        product.name = name
        product.price = price
        product.category = category
        db.session.commit()

        res = {
            product.id: {
                'name': product.name,
                'price': product.price,
                'category': product.category.name
            }
        }
        return jsonify(res)

    def delete(self, id):
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({'response': 'Success'}), 200

api.add_resource(
    ProductApi,
    '/api/product',
    '/api/product/<int:id>',
    '/api/product/<int:id>/<int:page>'
)
