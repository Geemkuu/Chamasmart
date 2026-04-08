import os
from fastapi import FastAPI
from supabase import create_client

app = FastAPI()

URL = "https://eymdckclisznzixcdket.supabase.co"
KEY = "PASTE_YOUR_SERVICE_ROLE_KEY_HERE"

supabase = create_client(URL, KEY)


@app.get("/api/balance")
def get_balance():
    # ... rest of your code
