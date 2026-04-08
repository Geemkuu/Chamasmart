from fastapi import FastAPI
from supabase import create_client
import os

app = FastAPI()

# Connect to your Supabase
URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_KEY")

if not URL or not KEY:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY environment variables")

supabase = create_client(URL, KEY)


@app.get("/api/balance")
def get_balance():
    try:
        res = supabase.table("transactions").select("amount").execute()
        total = sum(item['amount'] for item in res.data)
        return {"balance": total}
    except Exception as e:
        return {"error": str(e)}