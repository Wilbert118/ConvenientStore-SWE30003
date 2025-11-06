from app.db.connection import get_supabase
import os
from datetime import datetime

def insert_invoice(sale_id):
    invoice_url = f"/invoices/view/{sale_id}"
    data = {
        "sale_id": sale_id,
        "invoice_url": invoice_url,
        "generated_at": datetime.now().isoformat()
    }
    conn = get_supabase()
    res = conn.table("invoices").insert(data).execute()
    return res.data

def get_invoice_by_sale_id(sale_id):
    conn = get_supabase()
    res = conn.table("invoices").select("*").eq("sale_id", sale_id).execute()
    if res.data:
        return res.data[0]
    return None

def get_cart_items_by_sale_id(sale_id):
    conn = get_supabase()
    items = conn.table("cart_items").select("*").eq("sale_id", sale_id).execute().data
    return items

def get_payment_by_sale_id(sale_id):
    conn = get_supabase()
    sale_res = conn.table("sales").select("payment_id").eq("id", sale_id).execute()
    if not sale_res.data:
        return None
    payment_id = sale_res.data[0].get("payment_id")
    if not payment_id:
        return None
    res = conn.table("payments").select("method, status, paid_at").eq("id", payment_id).execute()
    if res.data:
        return res.data[0]
    return None 

def get_product_map():
    conn = get_supabase()
    products = conn.table("products").select("id", "name","price").execute().data
    return {p["id"]: {"name": p["name"], "price": float(p["price"])} for p in products}