from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from supabase import create_client
from pydantic import BaseModel
import os
import re

app = FastAPI()

# ============ SUPABASE CONFIG ============
URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_KEY")

if not URL or not KEY:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY environment variables")

supabase = create_client(URL, KEY)


# ============ VALIDATION & HELPERS ============
def validate_kenyan_phone(phone: str) -> str:
    """
    Validates and normalizes Kenyan phone numbers.
    Accepts formats: 254123456789, +254123456789, 0123456789
    Returns: normalized format starting with 254
    """
    phone = phone.strip()
    
    # Remove all non-digits except leading +
    if phone.startswith('+'):
        phone = phone.replace('+', '')
    phone = re.sub(r'\D', '', phone)
    
    # Handle different formats
    if phone.startswith('254'):
        pass  # Already in correct format
    elif phone.startswith('0'):
        phone = '254' + phone[1:]
    else:
        return None  # Invalid format
    
    # Validate length (254 + 9 remaining digits)
    if len(phone) != 12:
        return None
    
    return phone


def validate_amount(amount: float) -> bool:
    """Ensures amount is positive and valid"""
    return isinstance(amount, (int, float)) and amount > 0


def get_vibe_check(balance: float) -> str:
    """Returns sarcastic/encouraging message based on balance"""
    if balance == 0:
        return "The vault whispers into the void... 📭"
    elif balance < 5000:
        return "Baby steps to abundance 👶"
    elif balance < 50000:
        return "The group is cooking! 🔥"
    elif balance < 100000:
        return "We're building something real! 💪"
    else:
        return "This is how empires are built! 👑"


# ============ DATA MODELS ============
class DepositRequest(BaseModel):
    phone: str
    amount: float


# ============ API ENDPOINTS ============

@app.get("/")
def root():
    """Serve index.html"""
    return FileResponse("index.html")


@app.get("/api/balance")
def get_balance():
    """
    Calculate total vault balance by summing all transactions.
    Implements Append-Only integrity: never deletes, only reads.
    Includes Vibe Check for feedback.
    """
    try:
        res = supabase.table("transactions").select("amount").execute()
        
        # Sum all amounts (append-only ledger)
        total = sum(
            float(item['amount']) 
            for item in res.data 
            if validate_amount(item.get('amount'))
        )
        
        return {
            "balance": total,
            "vibe_check": get_vibe_check(total),
            "count": len(res.data)
        }
    except Exception as e:
        return {
            "error": str(e),
            "balance": 0,
            "vibe_check": "Connection lost to the vault 🔌"
        }


@app.post("/api/initiate-stk-push")
def initiate_stk_push(deposit: DepositRequest):
    """
    STK Push Placeholder - Ready for Safaricom Daraja API
    
    This endpoint:
    1. Validates the Kenyan phone number
    2. Validates the amount (must be positive)
    3. Saves the transaction to Supabase (append-only)
    4. Returns await confirmation (placeholder)
    
    Future: Wire to Safaricom Daraja API for actual M-Pesa STK
    """
    
    # Validate phone
    phone = validate_kenyan_phone(deposit.phone)
    if not phone:
        raise HTTPException(
            status_code=400, 
            detail="Invalid Kenyan phone number. Use format: 254723123456, +254723123456, or 0723123456"
        )
    
    # Validate amount
    if not validate_amount(deposit.amount):
        raise HTTPException(
            status_code=400,
            detail="Amount must be a positive number greater than 0"
        )
    
    if deposit.amount > 1000000:
        raise HTTPException(
            status_code=400,
            detail="Amount suspiciously high. Contact admin."
        )
    
    try:
        # APPEND-ONLY: Insert new transaction (never update/delete)
        res = supabase.table("transactions").insert({
            "phone": phone,
            "amount": deposit.amount,
            "status": "pending"
        }).execute()
        
        return {
            "status": "success",
            "message": f"STK Push initiated for {phone}",
            "amount": deposit.amount,
            "next_step": "Awaiting M-Pesa prompt on phone",
            "transaction_id": res.data[0].get('id') if res.data else None
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to initiate STK: {str(e)}"
        }


@app.get("/api/health")
def health_check():
    """Health check for monitoring"""
    return {"status": "ok", "service": "ChamaSmart Vault"}