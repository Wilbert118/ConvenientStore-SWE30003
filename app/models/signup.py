from app.db.connection import get_connection, get_supabase
import hashlib


def haspw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def signup(email, name, password, phone, address, role):
    conn = get_supabase()
    hashed_pw = haspw(password)
    email = email.strip().lower()
    data = {
        "email": email,
        "name": name,
        "password_hash": hashed_pw,
        "phone": phone,
        "address": address,
        "role": role
    }
    try:
        response = conn.table("users").insert(data).execute()
        return response
    except Exception as e:
        print(f"Error during signup: {e}")
        return None