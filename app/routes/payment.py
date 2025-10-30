from flask import Blueprint, render_template, request, redirect, session, flash
from app.models.payment import process_payment
from app.models.delivery import assign_delivery

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/payment', methods=['GET', 'POST'])
def payment():
    sale_id = session.get('sale_id')
    user_id = session.get('user').get('id')
    if sale_id is None:
        flash("No sale found. Please complete checkout first.")
        return redirect('/checkout')
    if request.method == 'POST':
        method = request.form['method']    
        payment = process_payment(user_id, sale_id, method)
        if payment:
            assign_delivery(sale_id)
            flash("Payment successful! Your order is being processed.")
            return redirect(f"/order/{sale_id}/status")
        else:
            flash("Payment failed. Please try again.")
    return render_template('payment.html', sale_id=sale_id)
            
        
