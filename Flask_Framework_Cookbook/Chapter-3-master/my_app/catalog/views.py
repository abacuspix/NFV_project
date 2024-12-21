from decimal import Decimal, InvalidOperation
from flask import request, Blueprint, jsonify
from my_app.catalog.models import Product
from sqlalchemy.orm import Session
from my_app.database import engine
from my_app.catalog.models import Product

catalog = Blueprint('catalog', __name__)


@catalog.route('/')
@catalog.route('/home')
def home():
    return "Welcome to the Catalog Home."


@catalog.route('/product/<key>')
def product(key):
    product = Product.objects.get_or_404(key=key)
    return 'Product - %s, $%s' % (product.name, product.price)


@catalog.route('/products')
def products():
    with Session(engine) as session:
        # Query all products
        products = session.query(Product).all()
        return jsonify([
            {
                'id': product.id,
                'name': product.name,
                'price': product.price
            }
            for product in products
        ])

@catalog.route('/product-create', methods=['POST'])
def create_product():
    name = request.form.get('name')
    key = request.form.get('key')
    price = request.form.get('price')

    if not name or not key or not price:
        abort(400, description="Missing required fields: 'name', 'key', or 'price'.")

    try:
        price = Decimal(price)
    except InvalidOperation:
        abort(400, description="Invalid price format. Must be a valid decimal.")

    with Session(engine) as session:
        product = Product(name=name, key=key, price=float(price))
        session.add(product)
        session.commit()

        # Access attributes before closing the session
        product_data = {
            'id': product.id,
            'name': product.name,
            'key': product.key,
            'price': product.price
        }

    return jsonify({'message': 'Product created successfully.', 'product': product_data}), 201