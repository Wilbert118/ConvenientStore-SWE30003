from app.db.connection import get_connection, get_supabase
import uuid

def fetch_all_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products ORDER BY created_at ASC;")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

def upload_product_image(file):
    conn = get_supabase()
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_bytes = file.read()
    conn.storage.from_("products").upload(filename, file_bytes)
    image_url = conn.storage.from_("products").get_public_url(filename)
    return image_url

def insert_product(name, price, category, stock, image_url):
    conn = get_supabase()
    conn.table("products").insert({
        "name": name,
        "price": price,
        "category": category,
        "stock": stock,
        "image_url": image_url
    }).execute()

def deduct_stock(sale_id):
    conn = get_supabase()
    try:
        items = conn.table('cart_items').select('product_id, quantity').eq('sale_id', sale_id).execute()
        
        for item in items.data:
            product_id = item['product_id']
            quantity_sold = item['quantity']
            product = conn.table('products').select('stock').eq('id', product_id).execute().data
            if not product:
                print(f"Product ID {product_id} not found.")
                return False
            current_stock = product[0]['stock']
            if quantity_sold > current_stock:
                print(f"Insufficient stock for product ID: {product_id}")
                return False
            
            new_stock = current_stock - quantity_sold
            conn.table('products').update({
                'stock': new_stock
            }).eq('id', product_id).execute()
        return True
    except Exception as e:
        print(f"Error deducting stock: {e}")
        return False    
                