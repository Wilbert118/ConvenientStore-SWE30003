from app.db.connection import get_connection, get_supabase
import uuid

def create_order(user_id, cart_data, shipping_details):
    conn = get_supabase()
    total_amount = sum(item['price'] * item['quantity'] for item in cart_data)
    print(f"This is the cart data: {cart_data}")
    sale_payload = {
        "user_id": user_id,
        "total": total_amount,
        "status": "pending"
    }
    try:
        sale_response = conn.table('sales').insert(sale_payload).execute()
        sale_id = sale_response.data[0]['id']
        cart_payload = [{
            "sale_id": sale_id,
            "user_id": user_id,
            "product_id": item['id'],
            "quantity": item['quantity']
        } for item in cart_data]

        conn.table('cart_items').insert(cart_payload).execute()

        shipping_payload = {
            "sale_id": sale_id,
            "recipient_name": shipping_details['recipient_name'],
            "address": shipping_details['address'],            
            "city": shipping_details['city'],
            "state": shipping_details.get('state'),
            "postcode": shipping_details['postcode'],           
            "phone": shipping_details['phone'],
            "notes": shipping_details.get('notes', '')
        }
        conn.table('shipping_details').insert(shipping_payload).execute()
        return sale_id
    except Exception as e:
        print(f"Error creating order: {e}")
        return None
    
def get_cart_items(sale_id):
    conn = get_supabase()
    try:
        response = conn.table('cart_items').select('*').eq('sale_id', sale_id).execute()
        return response.data
    except Exception as e:
        print(f"Error fetching cart items: {e}")
        return []
    