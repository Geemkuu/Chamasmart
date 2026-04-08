# ChamaSmart - Digital Ledger for Kenyan Savings Groups

A high-integrity, append-only digital ledger for managing Chama (savings group) finances with M-Pesa integration readiness.

## Features

✅ **Append-Only Ledger** - Transaction history is immutable. Never delete or edit records.
✅ **Real-time Balance** - Instant vault balance calculation from Supabase
✅ **STK Push Ready** - Placeholder for Safaricom Daraja M-Pesa integration
✅ **Kenyan Phone Validation** - Strict format validation for Kenyan numbers
✅ **Vibe Check** - Sarcastic balance feedback based on vault value
✅ **Mobile-First UI** - Optimized for Vivo y03 and similar devices
✅ **Dark Theme** - Slate-900 professional interface
✅ **Zero Trust** - Environment variable-based secrets management

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL)
- **Frontend**: HTML + Tailwind CSS
- **Deployment**: Vercel

## Local Setup

### 1. Clone & Install

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file (copy from `.env.example`):

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
```

### 3. Supabase Database

Create a `transactions` table in Supabase:

```sql
CREATE TABLE transactions (
  id SERIAL PRIMARY KEY,
  phone TEXT NOT NULL,
  amount DECIMAL(10, 2) NOT NULL,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Run Locally

```bash
uvicorn api.index:app --reload
```

Visit: `http://localhost:8000`

## Deployment to Vercel

### Prerequisites

- Vercel account (vercel.com)
- GitHub repository with this code
- Supabase project

### Steps

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Import to Vercel**
   - Go to vercel.com/new
   - Import your GitHub repository
   - Select "Other" framework

3. **Add Environment Variables**
   - Go to Settings → Environment Variables
   - Add:
     - `SUPABASE_URL`: Your Supabase project URL
     - `SUPABASE_KEY`: Your Supabase service role API key
   - Set both for Production

4. **Deploy**
   - Click "Deploy"
   - Wait for build to complete

## API Endpoints

### GET `/api/balance`
Returns current vault balance with transaction count and vibe check.

```json
{
  "balance": 150000,
  "vibe_check": "This is how empires are built! 👑",
  "count": 45
}
```

### POST `/api/initiate-stk-push`
Initiates M-Pesa STK Push (currently in test mode).

**Request:**
```json
{
  "phone": "254723123456",
  "amount": 5000
}
```

**Response:**
```json
{
  "status": "success",
  "message": "STK Push initiated for 254723123456",
  "amount": 5000,
  "next_step": "Awaiting M-Pesa prompt on phone",
  "transaction_id": "123abc"
}
```

## Phone Format Validation

Accepts:
- `254723123456` ✅
- `+254723123456` ✅
- `0723123456` ✅

Rejects:
- Invalid lengths
- Non-Kenyan numbers
- Non-numeric characters (except leading +)

## Append-Only Integrity

The system enforces:
1. ✅ Transactions are never deleted
2. ✅ Transactions are never edited
3. ✅ All amounts are validated (positive only)
4. ✅ Complete audit trail in database

## Future: Safaricom M-Pesa Integration

To enable real M-Pesa STK Push:

1. Register with Safaricom (mpesaapi.safaricom.co.ke)
2. Get Consumer Key and Consumer Secret
3. Update `/api/initiate-stk-push` with Daraja API calls
4. Add M-Pesa credentials to Vercel environment

## Troubleshooting

### 500 Error on Vercel
- ✅ Check environment variables are set in Vercel Settings
- ✅ Verify SUPABASE_URL and SUPABASE_KEY are correct
- ✅ Check Supabase table exists and is accessible

### "Invalid Kenyan phone" error
- ✅ Ensure phone starts with 254 or 0
- ✅ Remove spaces, hyphens, or parentheses
- ✅ Should be 12 digits starting with 254

### Balance shows 0 but has transactions
- ✅ Ensure `amount` column contains numeric values
- ✅ Check for NULL values in database
- ✅ Verify Supabase API key has read permissions

## Security Notes

🔒 **Never commit secrets** - Always use environment variables
🔒 **Service Role Key** - Use in trusted backend only, never in frontend
🔒 **Row-Level Security** - Enable RLS in Supabase for production
🔒 **Rate Limiting** - Add via Vercel middleware for production

## License

MIT - Built for Kenyan communities 🇰🇪
