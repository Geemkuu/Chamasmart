import os
from fastapi import FastAPI
from supabase import create_client

app = FastAPI()

# This is the 'Smart' way to handle keys
# It looks for the keys on Vercel first, then falls back to your local ones
URL = os.environ.get("SUPABASE_URL", "https://eymdckclisznzixcdket.supabase.co")
KEY = os.environ.get("SUPABASE_KEY", "PASTE_YOUR_ACTUAL_SERVICE_KEY_HERE")

supabase = create_client(URL, KEY)

@app.get("/api/balance")
def get_balance():
    # ... rest of your code
