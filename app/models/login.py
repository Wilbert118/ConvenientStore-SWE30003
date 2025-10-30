from app.db.connection import get_supabase
import hashlib


def haspw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def authenticate(email, password):
    conn = get_supabase()
    hashed_pw = haspw(password)
    email = email.strip().lower()
    try:
        response = conn.table("users").select("*").eq("email", email).execute()
        users = response.data
        if not users:
            return None
        
        stored_hashed= users[0]['password_hash']
        if stored_hashed == hashed_pw:
            return users[0]
        return None
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None