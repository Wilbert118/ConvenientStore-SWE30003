from flask import Blueprint, request, redirect, render_template
from app.models.product import upload_product_image, insert_product

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['image']
        name = request.form['name']
        price = float(request.form['price'])
        category = request.form['category']
        stock = int(request.form['stock'])

        image_url = upload_product_image(file)
        insert_product(name, price, category, stock, image_url)

        return redirect('/products')
    return render_template('upload.html')
