from flask import Blueprint, request, redirect, render_template, session, flash
from app.models.product import upload_product_image, insert_product

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    # Access control — only managers can add products
    user = session.get("user")
    if not user or user.get("role") != "manager":
        return redirect("/login")

    if request.method == 'POST':
        try:
            file = request.files['image']
            name = request.form['name']
            price = float(request.form['price'])
            category = request.form['category']
            stock = int(request.form['stock'])

            image_url = upload_product_image(file)
            insert_product(name, price, category, stock, image_url)

            flash("Product added successfully!")
            return redirect('/products')

        except Exception as e:
            flash(f"Failed to add product: {str(e)}")
            return redirect('/upload')

    return render_template('upload.html')
