from fastapi import FastAPI
from supabase import create_client

app = FastAPI()

# Your secure connection
supabase = create_client("URL", "SERVICE_KEY")

@app.get("/api/balance")
def get_balance():
    # Fast math from the cloud
    res = supabase.table("transactions").select("amount").execute()
    total = sum(item['amount'] for item in res.data)
    return {"balance": total, "vibe": "Chama is looking healthy! 🇰🇪"}