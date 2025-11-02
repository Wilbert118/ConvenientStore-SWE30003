from flask import Blueprint, render_template, flash, redirect, session, request
from app.models.delivery import order_status, overview_deliveries, change_delivery_status, get_delivery_details
from app.models.user import my_orders

delivery_bp = Blueprint('delivery', __name__)
order_status_bp = Blueprint('order_status', __name__)
@delivery_bp.route('/order/<int:sale_id>/status')
def order_status_view(sale_id):
    status = order_status(sale_id)
    return render_template('order_status.html', status=status, sale_id=sale_id)

@order_status_bp.route('/orders')
def my_orders_view():
    user_id = session.get('user').get('id')
    if not user_id:
        flash("Please log in to view your orders.")
        return redirect('/login')
    orders = my_orders(user_id)
    return render_template('my_orders.html', orders=orders)
    
@delivery_bp.route('/delivery/update/<int:sale_id>', methods=['GET','POST'])
def update_delivery_status(sale_id):
    user = session.get('user')
    if not user or user.get('role') != 'delivery':
        flash("Unauthorized access.")
        return redirect('/')
        
    if request.method == 'POST':
        new_status = request.form['status']
        success = change_delivery_status(sale_id, new_status)
        if success:
            flash("Delivery status updated successfully.")
            return redirect("/delivery/dashboard")
        else:
            flash("Failed to update delivery status.")
    delivery = get_delivery_details(sale_id)
    return render_template('update_delivery.html', delivery=delivery)

@delivery_bp.route('/delivery/dashboard')
def delivery_dashboard():
    user = session.get('user')
    if not user or user.get('role') != 'delivery':
        flash("Unauthorized access.")
        return redirect('/')
        
    user_id = user.get('id')
    deliveries = overview_deliveries(user_id)
    return render_template('delivery_dashboard.html', deliveries=deliveries)
    