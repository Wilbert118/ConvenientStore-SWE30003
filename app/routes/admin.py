from flask import Blueprint, render_template, flash, redirect, session, request
from app.models.user import manager_dashboard_overview, update_product, get_product_by_id, delete_product_by_id, update_status, update_delivery_status
from app.models.product import upload_product_image

manager_bp = Blueprint('manager', __name__) 

@manager_bp.route('/manager/dashboard')
def manager_dashboard():
    user = session.get('user')
    if not user or user.get('role') != 'manager':
        flash("Access denied.")
        return redirect('/')
    dashboard_data = manager_dashboard_overview()
        
    return render_template('manager_dashboard.html', **dashboard_data)

@manager_bp.route('/manager/product/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    user = session.get('user')
    if not user or user.get('role') != 'manager':
        flash("Access denied.")
        return redirect('/')
    success = delete_product_by_id(product_id)
    if success:
        flash("Product deleted successfully.")
    else:
        flash("Failed to delete product.")
    return redirect('/manager/dashboard')
    
    
@manager_bp.route('/manager/product/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    user = session.get('user')
    if not user or user.get('role') != 'manager':
        flash("Access denied.")
        return redirect('/')
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        image = request.files.get('image')
        if image and image.filename:
            image_url = upload_product_image(image)
            success = update_product(product_id, name, price, stock, image_url)
        else:
            success = update_product(product_id, name, price, stock)
        if success:
            flash("Product updated successfully.")
            return redirect('/manager/dashboard')
        else:
            flash("Failed to update product.")
            
    product = get_product_by_id(product_id)
    if not product:
        flash("Product not found.")
        return redirect('/manager/dashboard')
    return render_template('edit_product.html', product=product)
    
@manager_bp.route('/manager/sale/update/<int:sale_id>', methods=['POST'])
def update_sale_status(sale_id):
    user = session.get('user')
    if not user or user.get('role') != 'manager':
        flash("Access denied.")
        return redirect('/')
    new_status = request.form['status']
    
    update = update_status(sale_id, new_status)
    if update:
        flash("Sale status updated successfully.")
    else:
        flash("Failed to update sale status.")
    return redirect('/manager/dashboard')
    
@manager_bp.route('/manager/delivery/update/<int:delivery_id>', methods=['POST'])
def update_delivery_status_manager(delivery_id):
    user = session.get('user')
    if not user or user.get('role') != 'manager':
        flash("Access denied.")
        return redirect('/')
    new_status = request.form.get("status")
    
    update = update_delivery_status(delivery_id, new_status)
    if update:
        flash("Delivery status updated successfully.")
    else:
        flash("Failed to update delivery status.")
    return redirect('/manager/dashboard')