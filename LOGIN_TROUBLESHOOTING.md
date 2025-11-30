# 🔐 DragonFruit Login Issues - Troubleshooting Guide

## Error: 401 Unauthorized - "Not authenticated"

This error occurs when `GET /api/auth/me` is called but the session cookie isn't present or valid.

## Root Causes & Solutions

### 1. **User Not Logged In**
**Symptom:** 401 error on dashboard load  
**Solution:** You need to login first!

```bash
# Steps to test login:
1. Go to http://localhost:3000/login
2. Enter valid credentials:
   - Email: admin@example.com  (or any valid user)
   - Password: your_password
3. Click "Sign In"
4. Should redirect to /dashboard
```

### 2. **Cookie Not Being Sent**
**Symptom:** 401 error even after successful login  
**Solution:** Check if credentials are being included

#### Frontend - Fixed in `lib/api.ts`:
```typescript
credentials: options?.credentials || 'include'  // ✅ Now defaults to 'include'
```

#### Backend - Check CORS in `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,  # ✅ MUST BE TRUE!
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. **Session Expired**
**Symptom:** Login works, but get 401 after some time  
**Solution:** Sessions expire after 1 hour by default (see `auth/session.py`)

```python
# Session expires in 1 hour
expires_at: datetime.utcnow() + timedelta(hours=1)
```

**To extend:** Modify `auth/session.py`:
```python
expires_at: datetime.utcnow() + timedelta(hours=24)  # 24 hours
```

### 4. **Backend Not Running**
**Symptom:** Connection refused or 404 errors  
**Solution:** Start the backend server

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

### 5. **Wrong API URL in Frontend**
**Symptom:** 404 or CORS errors  
**Solution:** Check `.env.local` in dashboard

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## Files Modified to Fix Login

✅ `src/lib/api.ts` - Now always sends credentials  
✅ `src/lib/auth.ts` - Better error logging  
✅ `src/app/dashboard/components/AuthGuard.tsx` - Better loading state

## Testing Checklist

- [ ] Backend running: `uvicorn main:app --reload`
- [ ] Dashboard running: `npm run dev`
- [ ] Frontend points to correct API URL (`.env.local`)
- [ ] CORS middleware has `allow_credentials=True`
- [ ] User account exists in database
- [ ] Password is correct
- [ ] Cookies are being saved (check DevTools → Application → Cookies)

## Browser DevTools Debug Steps

1. **Open DevTools** (F12)
2. **Go to Network tab**
3. **Attempt login**
4. **Look for:** `/api/auth/login` request
   - Status should be **200**
   - Response Headers should include **Set-Cookie: session_id=...**
5. **After login, check:** `/api/auth/me` request
   - Should see **Cookie: session_id=...** in Request Headers
   - Status should be **200**

## Quick Diagnostic Commands

### Check if backend is responding:
```bash
curl http://127.0.0.1:8000/health
# Should return: {"status":"ok","database":"..."}
```

### Check if user exists:
```bash
# In backend Python shell
from controllers.UserController import get_user_by_username_or_email
user = get_user_by_username_or_email("admin@example.com")
print(user)
```

### Test session creation:
```bash
# In backend Python shell
from auth.session import create_session, get_session
session_id = create_session("user-uid-123")
print(get_session(session_id))
```

## API Endpoints Reference

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/api/auth/login` | POST | ❌ | Login and receive session_id cookie |
| `/api/auth/me` | GET | ✅ | Get current user info (requires session) |
| `/api/auth/logout` | POST | ✅ | Logout and clear session |
| `/api/auth/update-username` | PUT | ✅ | Change username |
| `/api/auth/update-password` | PUT | ✅ | Change password |

## Common Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| `401 Not authenticated` | No session_id cookie | Login first |
| `401 Session expired` | Session > 1 hour old | Login again |
| `401 User not found` | User deleted or wrong UID | Check user exists |
| `404` | Wrong API URL | Update `.env.local` |
| `CORS error` | Backend missing credentials | Add `allow_credentials=True` |

## Success Indicators

✅ Login successful when:
- You see **Status 200** for `/api/auth/login`
- Response includes **Set-Cookie header**
- You're redirected to `/dashboard`
- Dashboard loads data without 401 errors

---

**Status:** ✅ Login flow now has proper credential handling and better error messages!
