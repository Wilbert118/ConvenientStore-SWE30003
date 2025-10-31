from app.db.connection import get_connection, get_supabase

def my_orders(user_id):
    conn = get_supabase()
    sales = conn.table('sales').select('*').eq('user_id', user_id).order("created_at", desc=True).execute().data
    
    orders = []
    for sale in sales:
        delivery = conn.table('deliveries').select('*').eq("sale_id", sale["id"]).execute().data
        if not delivery:
            print(f"No delivery info found for sale ID: {sale['id']}")
            continue
        deliver_personnel = conn.table('users').select('name, phone').eq("id", delivery[0]["delivery_person_id"]).execute().data
        orders.append({
            "sale_id": sale["id"],
            "created_at": sale["created_at"],
            "tracking_number": delivery[0]["tracking_number"] if delivery else "Not assigned",
            "status": delivery[0]["status"],
            "delivery_personnel": deliver_personnel[0] if deliver_personnel else None
        })
    return orders