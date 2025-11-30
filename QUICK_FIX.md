# Quick Fix for Your Friend - 404 API Error

## TL;DR - What to Do

```bash
# 1. Go to dashboard folder
cd dragonfruit-dashboard

# 2. Create .env.local file (copy from example)
cp .env.example .env.local

# 3. Edit .env.local and change this line:
NEXT_PUBLIC_API_URL=http://YOUR_BACKEND_SERVER_IP:8000

# Example: If backend is at 192.168.1.100
NEXT_PUBLIC_API_URL=http://192.168.1.100:8000

# 4. Restart dashboard
npm run dev

# 5. Done! Dashboard should now connect to your backend
```

## What Was The Problem?

The dashboard was **hardcoded** to only connect to `http://127.0.0.1:8000` (localhost). When your friend runs it on a different machine, localhost doesn't work because the backend is on another computer.

## What Was Fixed?

✅ Changed from hardcoded URLs to **environment variable-based configuration**  
✅ Now you can configure ANY backend server IP/domain  
✅ Works for localhost, remote servers, and cloud deployments

## Files Updated

- `src/app/dashboard/page.tsx` - Main dashboard page
- `src/app/dashboard/setting/page.tsx` - Settings page
- `.env.local` - Your configuration (you)
- `.env.example` - Template for others

## Backend Requirements

Make sure your backend allows CORS from your frontend. In `main.py`:

```python
allow_origins=[
    "http://localhost:3000",           # Your machine
    "http://192.168.1.100:3000",      # Your friend's machine IP
    # Add your actual IPs here
]
```

---

**Status:** ✅ Dashboard now supports configurable API URLs!
