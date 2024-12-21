# coding:utf-8

from flask import Flask, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Use a strong secret key from environment variables or a configuration file
app.config['SECRET_KEY'] = '\xa6\xb5\x0e\x7f\xd3}\x0b-\xaa\x03\x03\x82\x10\xbe\x1e0u\x93,{\xd4Z\xa3\x8f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ex05.sqlite'
db = SQLAlchemy(app)


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(30), unique=True)
    name = db.Column(db.String(255), nullable=False)

    def __str__(self):
        return self.name


@app.route("/cart/add/<sku>")
def add_to_cart_view(sku):
    product = Product.query.filter_by(sku=sku).first()

    if product is not None:
        session['cart'] = session.get('cart', {})
        item = session['cart'].get(product.sku, {})
        item['qty'] = item.get('qty', 0) + 1
        session['cart'][product.sku] = item
        flash(f'{product} added to cart. Total: {item["qty"]}')

    return render_template('cart.html')


def init_db():
    """
    Initializes and populates the database.
    """
    db.create_all()

    if Product.query.count() == 0:
        db.session.add_all([
            Product(sku='010', name='Boots'),
            Product(sku='020', name='Gauntlets'),
            Product(sku='030', name='Helmets'),
        ])
        db.session.commit()


if __name__ == '__main__':
    app.debug = True

    # Initialize the database if running the app directly
    with app.app_context():
        init_db()

    app.run()
