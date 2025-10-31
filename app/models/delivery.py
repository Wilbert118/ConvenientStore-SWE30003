from app.db.connection import get_supabase
import random
import uuid
import datetime

def generate_tracking_number():
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_part = uuid.uuid4().hex[:6].upper()
    return f"TRK-{timestamp}-{random_part}"

def assign_delivery(sale_id):
    conn = get_supabase()
    shipping_id = conn.table('shipping_details').select('id').eq('sale_id', sale_id).execute().data[0]['id']
    personnel = conn.table("users").select("id").eq("role", "delivery").execute().data

    
    active = conn.table("deliveries").select("delivery_person_id").eq("status", "pending").execute().data
    active_ids = {d["delivery_person_id"] for d in active}

    
    available = [p["id"] for p in personnel if p["id"] not in active_ids]

    
    if available:
        chosen_id = available[0]  
    else:
        chosen_id = random.choice([p["id"] for p in personnel])  
        
    delivery_payload = {
        "sale_id": sale_id,
        "shipping_id": shipping_id,
        "tracking_number": generate_tracking_number(),
        "delivery_person_id": chosen_id,
        "status": "pending"
    }
    
    conn.table('deliveries').insert(delivery_payload).execute()
    return True

def order_status(sale_id):
    conn = get_supabase()
    delivery = conn.table("deliveries").select("*").eq("sale_id", sale_id).execute().data[0]
    shipping = conn.table("shipping_details").select("*").eq("sale_id", sale_id).execute().data[0]
    items = conn.table("cart_items").select("*").eq("sale_id", sale_id).execute().data
    product_ids = [item["product_id"] for item in items]
    products = conn.table("products").select("id", "name").in_("id", product_ids).execute().data


    product_lookup = {p["id"]: p["name"] for p in products}


    for item in items:
        item["product_name"] = product_lookup.get(item["product_id"], "Unknown Product")
    personnel = conn.table("users").select("*").eq("id", delivery["delivery_person_id"]).execute().data[0]
    return {
        "delivery": delivery,
        "shipping": shipping,
        "items": items,
        "delivery_person": personnel
    }
    
def change_delivery_status(sale_id, new_status):
    conn = get_supabase()
    try:
        conn.table("deliveries").update({
            "status": new_status,
            "updated_at": datetime.datetime.now().isoformat()
        }).eq("sale_id", sale_id).execute()
        return True
    except Exception as e:
        print(f"Error updating delivery status: {e}")
        return False

def overview_deliveries(delivery_person_id):
    conn = get_supabase()
    deliveries = conn.table("deliveries").select("*").eq("delivery_person_id", delivery_person_id).order("updated_at", desc=True).execute().data
    return deliveries

def get_delivery_details(sale_id):
    conn = get_supabase()
    delivery = conn.table("deliveries").select("*").eq("sale_id", sale_id).execute().data
    if delivery:
        return delivery[0]
    return None