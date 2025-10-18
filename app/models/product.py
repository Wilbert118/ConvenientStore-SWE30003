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
