from fastapi import FastAPI
from supabase import create_client
import os

app = FastAPI()

# Connect to your Supabase
URL = "https://eymdckclisznzixcdket.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV5bWRja2NsaXN6bnppeGNka2V0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NTY1MDY1MSwiZXhwIjoyMDkxMjI2NjUxfQ.d9cf0ypTDNVU9YASP91rqvV4mN_xZ_IvJ0qpPtWW98I"
supabase = create_client(URL, KEY)

@app.get("/api/balance")
def get_balance():
    try:
        res = supabase.table("transactions").select("amount").execute()
        total = sum(item['amount'] for item in res.data)
        return {"balance": total}
    except Exception as e:
        return {"error": str(e)}