# 🐉 DragonFruit Dashboard - API Configuration Guide

## Problem: 404 Error on Dashboard

Your friend is getting a **404 API error** because the dashboard is hardcoded to call `http://127.0.0.1:8000` or `http://localhost:8000`, but the backend might be running on a different machine or IP address.

## Solution: Configure API URL via Environment Variable

### For Your Friend (Remote Machine)

1. **Navigate to dashboard directory:**
   ```bash
   cd dragonfruit-dashboard
   ```

2. **Create `.env.local` file:**
   ```bash
   cp .env.example .env.local
   ```

3. **Edit `.env.local` and update the API URL:**
   ```env
   # Replace 127.0.0.1 with your backend server's IP or domain
   NEXT_PUBLIC_API_URL=http://192.168.1.100:8000
   # OR
   NEXT_PUBLIC_API_URL=http://your-backend-server-ip:8000
   ```

4. **Restart the dashboard development server:**
   ```bash
   npm run dev
   ```

### For You (Local Machine)

Your `.env.local` is already configured correctly:
```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## What Was Fixed

### ✅ Changes Made:

1. **Dashboard Page** (`src/app/dashboard/page.tsx`)
   - ❌ Before: Hardcoded `fetch('http://127.0.0.1:8000/api/gradingresult/all')`
   - ✅ After: Uses environment variable `process.env.NEXT_PUBLIC_API_URL`

2. **Settings Page** (`src/app/dashboard/setting/page.tsx`)
   - ❌ Before: Hardcoded `fetch("http://localhost:8000/api/auth/update-username")`
   - ✅ After: Uses environment variable `process.env.NEXT_PUBLIC_API_URL`
   - ❌ Before: Hardcoded `fetch("http://localhost:8000/api/auth/update-password")`
   - ✅ After: Uses environment variable `process.env.NEXT_PUBLIC_API_URL`

3. **Created Configuration Files:**
   - ✅ `.env.local` - Development configuration (for you)
   - ✅ `.env.example` - Template for your friend

## Backend CORS Configuration

**IMPORTANT:** Make sure your FastAPI backend allows requests from your frontend's origin. Update `main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # Local frontend
        "http://127.0.0.1:3000",      
        "http://192.168.1.100:3000",  # Your friend's machine
        "http://your-server-ip:3000", # Add your server IP if different
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Testing

1. **Local (You):**
   ```bash
   # Backend
   cd backend && uvicorn main:app --reload
   
   # Dashboard (in another terminal)
   cd dragonfruit-dashboard && npm run dev
   
   # Access: http://localhost:3000
   ```

2. **Remote (Your Friend):**
   ```bash
   # Make sure backend is accessible at:
   # http://backend-server-ip:8000
   
   # Update .env.local with correct IP
   NEXT_PUBLIC_API_URL=http://backend-server-ip:8000
   
   # Start dashboard
   npm run dev
   
   # Access from their machine
   # http://localhost:3000 or http://their-machine-ip:3000
   ```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Still getting 404 | Check `.env.local` has correct API URL |
| CORS error | Update `allow_origins` in FastAPI CORS middleware |
| Connection refused | Make sure backend is running and accessible |
| Changes not applied | Delete `.next` folder and restart dev server |

## Files Modified

- ✅ `/dragonfruit-dashboard/src/app/dashboard/page.tsx`
- ✅ `/dragonfruit-dashboard/src/app/dashboard/setting/page.tsx`
- ✅ `/dragonfruit-dashboard/.env.local` (created)
- ✅ `/dragonfruit-dashboard/.env.example` (created)

---

**Status:** ✅ All configuration files created and dashboard updated to use environment variables for API URL!
