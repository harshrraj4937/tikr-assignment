# 🚀 Quick Start Guide - Tikr Frontend

Get up and running with the Tikr authentication frontend in under 5 minutes!

## Prerequisites Check

✅ Node.js 16+ installed (`node --version`)  
✅ Backend running on port 8000  
✅ Database seeded with test users  

## Step 1: Install Dependencies (First Time Only)

```bash
cd frontend/UI
npm install
```

⏱️ Takes about 20-30 seconds

## Step 2: Start the Backend

```bash
# From project root
./start_backend.sh
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 3: Seed Database (First Time Only)

In a new terminal:

```bash
cd backend
python seed_data.py
```

You should see:
```
✅ Database seeded successfully!

Test accounts:
  Admin:   admin@dealflow.com / admin123
  Analyst: analyst@dealflow.com / analyst123
  Partner: partner@dealflow.com / partner123
```

## Step 4: Start the Frontend

```bash
# From project root
./start_frontend.sh
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

## Step 5: Test It Out! 🎉

1. **Open your browser**: http://localhost:5173

2. **Login as Admin**:
   - Email: `admin@dealflow.com`
   - Password: `admin123`
   - Click "Log In"

3. **See your dashboard**:
   - User info displayed
   - Red "Admin" tag (Level 3)
   - Full permissions listed
   - Role capabilities shown

4. **Test logout**:
   - Click the red "Logout" button
   - Redirected back to login page

5. **Try other roles**:
   - Analyst: `analyst@dealflow.com` / `analyst123` (Blue tag)
   - Partner: `partner@dealflow.com` / `partner123` (Green tag)

## 🎯 What You Should See

### Login Page
- Purple gradient background
- "Welcome to Tikr" title
- Email and password fields
- Blue "Log In" button

### Dashboard (After Login)
- User avatar and welcome message
- User information card:
  - Email, username, name
  - Account creation date
- Role & permissions card:
  - Color-coded role tag
  - Hierarchy level
  - Permission tags
  - Role capabilities list
- Red logout button

## 🐛 Troubleshooting

### "Cannot connect to backend"
**Fix**: Make sure backend is running on port 8000
```bash
curl http://localhost:8000/docs
```

### "Incorrect email or password"
**Fix**: Make sure you ran the seed script
```bash
cd backend
python seed_data.py
```

### "Port 5173 already in use"
**Fix**: Kill the process
```bash
lsof -ti:5173 | xargs kill -9
```

### "Module not found" errors
**Fix**: Reinstall dependencies
```bash
cd frontend/UI
rm -rf node_modules package-lock.json
npm install
```

## 📝 Test Credentials

| Role | Email | Password | Tag Color |
|------|-------|----------|-----------|
| Admin | admin@dealflow.com | admin123 | 🔴 Red |
| Analyst | analyst@dealflow.com | analyst123 | 🔵 Blue |
| Partner | partner@dealflow.com | partner123 | 🟢 Green |

## ✨ Features to Test

- [x] Login with valid credentials
- [x] See error with invalid credentials
- [x] View user information
- [x] See role-specific permissions
- [x] Logout functionality
- [x] Protected routes (try accessing /dashboard without login)
- [x] Auto-redirect (try accessing /login when logged in)

## 🎨 Tech Stack

- **Frontend**: React 18 + TypeScript + Vite
- **UI Library**: Ant Design 5
- **HTTP Client**: Axios
- **Routing**: React Router 6
- **Backend**: FastAPI (Python)
- **Database**: SQLite with Django ORM

## 📚 Next Steps

Now that authentication is working, you can:

1. Explore the code in `frontend/UI/src/`
2. Read the detailed docs in `FRONTEND_SETUP.md`
3. Check out `FEATURES.md` for UI/UX details
4. Start building the deal pipeline features
5. Add IC memo functionality
6. Implement comments and voting

## 🆘 Need Help?

- Check browser console for errors (F12)
- Look at network tab for failed API calls
- Review backend logs for server errors
- Read `FRONTEND_SETUP.md` for detailed troubleshooting

## 🎉 Success Criteria

You've successfully set up the frontend if:

✅ Login page loads at http://localhost:5173  
✅ Can login with test credentials  
✅ Dashboard shows user information  
✅ Role tag displays with correct color  
✅ Logout works and redirects to login  
✅ Protected routes redirect when not authenticated  

**Congratulations! Your authentication system is working! 🚀**

