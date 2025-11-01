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

def manager_dashboard_overview():
    conn = get_supabase()
    products = conn.table("products").select("*").execute().data
    users = conn.table("users").select("id, name, role").order("id", desc=False).execute().data
    deliveries = conn.table("deliveries").select("*").order("id", desc=False).execute().data
    sales = conn.table("sales").select("*").order("id", desc=False).execute().data
    total_sales = len(sales)
    total_revenue = sum(sale["total"] for sale in sales)
    user_map = {user["id"]: user["name"] for user in users}
    
    for sale in sales:
        sale["customer_name"] = user_map.get(sale["user_id"], "Unknown User")
        
    for delivery in deliveries:
        delivery["delivery_person"] = user_map.get(delivery["delivery_person_id"], "Unknown Driver")

    dashboard_data = {
        "total_products": len(products),
        "total_orders": len(sales),
        "total_users": len(users),
        "total_deliveries": len(deliveries),
        "total_sales": total_sales,
        "total_revenue": total_revenue,
        "products": products,
        "sales": sales,
        "users": users,
        "deliveries": deliveries
    }
    return dashboard_data

def update_product(product_id, name, price, stock, image_url=None):
    conn  = get_supabase()
    update_data = {
        "name": name,
        "price": price,
        "stock": stock
    }
    if image_url:
        update_data["image_url"] = image_url
    product = conn.table('products').update(update_data).eq('id', product_id).execute().data
    if not product:
        return False
    return True
    
    
def get_product_by_id(product_id):
    conn = get_supabase()
    product = conn.table('products').select('*').eq('id', product_id).execute().data
    if not product:
        return None
    return product[0]

def delete_product_by_id(product_id):
    conn = get_supabase()
    result = conn.table('products').delete().eq('id', product_id).execute().data
    if not result:
        return False
    return True

def update_status(sale_id, new_status):
    conn = get_supabase()
    try:
        conn.table('sales').update({
            'status': new_status
        }).eq('id', sale_id).execute()
        return True
    except Exception as e:
        print(f"Error updating sale status: {e}")
        return False
    
def update_delivery_status(delivery_id, new_status):
    conn = get_supabase()
    try:
        conn.table('deliveries').update({
            'status': new_status
        }).eq('id', delivery_id).execute()
        return True
    except Exception as e:
        print(f"Error updating delivery status: {e}")
        return False