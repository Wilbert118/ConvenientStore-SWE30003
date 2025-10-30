from app.db.connection import get_supabase

def process_payment(user_id, sale_id, method):
    conn = get_supabase()
    payment_payload = {
        "user_id": user_id,
        "method": method,
        "status": "success"
    }
    try:
        payment = conn.table('payments').insert(payment_payload).execute()
        if payment.data:
            payment_id = payment.data[0]['id']
            conn.table('sales').update({
                "status": "paid",
                "payment_id": payment_id
            }).eq("id", sale_id).execute()
            return True
        else:
            print("Payment insert failed:", payment)
            return False
    except Exception as e:
        print(f"Error processing payment: {e}")
        return False
