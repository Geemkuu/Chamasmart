from fastapi import FastAPI
from supabase import create_client
import os

# THIS IS THE ENTRYPOINT VERCEL IS LOOKING FOR
app = FastAPI() 

URL = os.environ.get("SUPABASE_URL", "https://eymdckclisznzixcdket.supabase.co")
KEY = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV5bWRja2NsaXN6bnppeGNka2V0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NTY1MDY1MSwiZXhwIjoyMDkxMjI2NjUxfQ.d9cf0ypTDNVU9YASP91rqvV4mN_xZ_IvJ0qpPtWW98I")

supabase = create_client(URL, KEY)

@app.get("/api/balance")
def get_balance():
    # your logic here...
    return {"status": "success"}