import os
from dotenv import load_dotenv
import psycopg2
from supabase import create_client

load_dotenv()

def get_connection():
    return psycopg2.connect(
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PW"),
        host = os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME")
    )
def get_supabase():
    return create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))