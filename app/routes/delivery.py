from flask import Blueprint, render_template
from app.models.delivery import order_status

delivery_bp = Blueprint('delivery', __name__)
@delivery_bp.route('/order/<int:sale_id>/status')
def order_status_view(sale_id):
    status = order_status(sale_id)
    return render_template('order_status.html', status=status)