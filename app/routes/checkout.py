import json
from flask import Blueprint, render_template, request, redirect, session, flash
from app.models.order import create_order, get_cart_items


checkout_bp = Blueprint('checkout', __name__)

@checkout_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        user_id = session.get('user').get('id')
        print(f"User ID from session: {user_id}")
        if user_id is None:
            flash("You must be logged in to checkout.")
            return redirect('/login')
        cart_data = json.loads(request.form['cart'])
        shipping_details = {
            'address': request.form['address'],
            'phone': request.form['phone'],
            'recipient_name': request.form['name'],
            'postcode': request.form['postal_code'],
            'city': request.form['city'],
            'state': request.form['state'],
            'notes': request.form.get('notes', '')
        }
        try:
            print("Initiating checkout process...")
            sale_id = create_order(user_id, cart_data, shipping_details)
            if sale_id:
                print(f"Order created successfully with sale_id: {sale_id}")
                session['sale_id'] = sale_id
                return redirect('/payment')
        except Exception as e:
            flash(f"Checkout failed: {str(e)}")
            return redirect('/cart')
    return render_template('checkout.html')