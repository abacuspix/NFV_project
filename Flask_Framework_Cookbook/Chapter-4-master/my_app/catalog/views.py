from functools import wraps

from flask import request, Blueprint, render_template, jsonify, flash, \
    redirect, url_for
from sqlalchemy.sql import join

from my_app import db, app
from my_app.catalog.models import Product, Category

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
        'products.html', products=products.paginate(page=page, per_page=10, error_out=False)
    )


from flask import request, render_template, redirect, url_for, flash
from my_app import db
from my_app.catalog.models import Category

@catalog.route('/category-create', methods=['POST'])
def create_category():
    # Get category name from form data
    name = request.form.get('name')
    
    # Validate input
    if not name:
        flash("Category name is required.", "danger")
        return redirect(url_for('catalog.categories'))
    
    # Check for duplicate names (optional)
    existing_category = Category.query.filter_by(name=name).first()
    if existing_category:
        flash("Category with this name already exists.", "warning")
        return redirect(url_for('catalog.categories'))

    # Create and save new category
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    
    flash(f"Category '{name}' created successfully.", "success")
    return redirect(url_for('catalog.categories'))


@catalog.route('/category/<int:id>')
def category(id):
    # Fetch category or 404 if not found
    category = Category.query.get_or_404(id)
    return render_template('category.html', category=category)


@catalog.route('/categories')
def categories():
    # Paginate categories (optional)
    page = request.args.get('page', 1, type=int)
    categories = Category.query.paginate(page=page, per_page=10, error_out=False)
    
    return render_template('categories.html', categories=categories)
