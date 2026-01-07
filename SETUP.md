# Quick Setup Guide

## Prerequisites
- Python 3.11+
- Node.js 18+
- pip and npm

## Quick Start (Development)

### Option 1: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python seed_data.py
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend/UI
npm install
npm run dev
```

### Option 2: Using Start Scripts

**Terminal 1:**
```bash
./start_backend.sh
```

**Terminal 2:**
```bash
./start_frontend.sh
```

## Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Test Accounts

Login with these pre-configured accounts:

1. **Admin**
   - Email: `admin@dealflow.com`
   - Password: `admin123`

2. **Analyst**
   - Email: `analyst@dealflow.com`
   - Password: `analyst123`

3. **Partner**
   - Email: `partner@dealflow.com`
   - Password: `partner123`

## Quick Test Flow

1. **Login as Analyst** (analyst@dealflow.com / analyst123)
2. **Create a new deal**: Click "New Deal" button
3. **Drag the deal** across stages using the Kanban board
4. **Open the deal** by clicking on the card
5. **Add a comment** at the bottom of the deal page
6. **Create IC Memo**: Click "IC Memo" button and fill in sections
7. **Save memo**: Click "Save New Version"
8. **Logout** and login as Partner (partner@dealflow.com / partner123)
9. **Vote on the deal**: Open deal → Click "Cast Vote" → Choose Approve/Decline
10. **Login as Admin** (admin@dealflow.com / admin123)
11. **Manage users**: Navigate to "Users" in sidebar

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**Database errors:**
```bash
cd backend
rm db.sqlite3
python manage.py migrate
python seed_data.py
```

### Frontend Issues

**Dependencies error:**
```bash
cd frontend/UI
rm -rf node_modules package-lock.json
npm install
```

**Port already in use:**
```bash
# Find and kill process on port 5173
lsof -ti:5173 | xargs kill -9
```

## Features to Test

✅ **Authentication**
- Login with different roles
- JWT token persistence
- Auto-redirect on 401

✅ **Deal Management**
- Create new deals (Analyst/Admin only)
- Edit deal details (Owner/Admin only)
- Drag-and-drop between stages

✅ **IC Memos**
- Create memo with 6 sections
- Version history
- View previous versions

✅ **Collaboration**
- Add comments (all users)
- Vote on deals (Partner/Admin only)
- View activity timeline

✅ **User Management**
- Create users (Admin only)
- Assign roles
- Edit user details

## API Testing

You can also test the API directly using the interactive documentation:

1. Open http://localhost:8000/docs
2. Click "Authorize" button
3. Login via `/api/auth/login` endpoint
4. Copy the `access_token` from response
5. Paste in authorization modal (format: `Bearer <token>`)
6. Test any endpoint

Enjoy! 🚀

