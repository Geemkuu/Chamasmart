import os
from fastapi import FastAPI
from supabase import create_client

app = FastAPI()

# Your secure connection
supabase = create_client("URL", "SERVICE_KEY")

@app.get("/api/balance")
def get_balance():
    # ... rest of your code
