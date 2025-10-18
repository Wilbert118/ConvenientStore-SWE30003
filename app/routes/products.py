from flask import Blueprint, render_template
from app.models.product import fetch_all_products
products_bp = Blueprint('products', __name__)

@products_bp.route('/products')
def show_products():
    products = fetch_all_products()
    return render_template('products.html', products=products)
