# Frontend Setup Guide

This guide will help you set up and run the Tikr frontend application.

## Prerequisites

- Node.js 16+ and npm installed
- Backend API running on `http://localhost:7000`

## Quick Start

### 1. Install Dependencies

```bash
cd frontend/UI
npm install
```

### 2. Start the Development Server

```bash
npm run dev
```

Or from the project root:

```bash
./start_frontend.sh
```

The frontend will be available at: **http://localhost:5173**

## Test Accounts

Use these credentials to test different user roles:

| Role | Email | Password |
|------|-------|----------|
| **Admin** | admin@dealflow.com | admin123 |
| **Analyst** | analyst@dealflow.com | analyst123 |
| **Partner** | partner@dealflow.com | partner123 |

## Features Implemented

### ✅ Authentication
- Email/password login form with validation
- JWT token management
- Automatic token refresh
- Secure logout

### ✅ User Dashboard
- Display user information (email, username, name)
- Show user role with color-coded tags:
  - 🔴 **Admin** (Level 3) - Red tag
  - 🔵 **Analyst** (Level 2) - Blue tag
  - 🟢 **Partner** (Level 1) - Green tag
- Display role permissions
- Show role capabilities description
- Account creation date

### ✅ Protected Routes
- Automatic redirect to login if not authenticated
- Automatic redirect to dashboard if already logged in
- Loading states during authentication checks

### ✅ Modern UI
- Beautiful gradient backgrounds
- Responsive design
- Ant Design components
- Clean and professional interface

## Project Structure

```
frontend/UI/
├── src/
│   ├── components/
│   │   └── ProtectedRoute.tsx      # Route protection wrapper
│   ├── contexts/
│   │   └── AuthContext.tsx         # Authentication state management
│   ├── pages/
│   │   ├── Login.tsx               # Login page
│   │   └── Dashboard.tsx           # User dashboard
│   ├── services/
│   │   └── api.ts                  # API client with axios
│   ├── types/
│   │   └── auth.ts                 # TypeScript type definitions
│   ├── App.tsx                     # Main app with routing
│   ├── main.tsx                    # Entry point
│   └── index.css                   # Global styles
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts                  # Vite configuration with proxy
└── README.md
```

## How It Works

### Authentication Flow

1. **Login**: User enters email and password
2. **API Call**: Credentials sent to `POST /auth/login`
3. **Token Storage**: JWT token and user data stored in localStorage
4. **Redirect**: User redirected to dashboard
5. **Protected Access**: All subsequent API calls include the token

### API Integration

The frontend communicates with these backend endpoints:

- `POST /auth/login` - Authenticate user and get JWT token
- `GET /auth/me` - Get current user information

API requests are proxied through Vite in development:
- `/auth/*` → `http://localhost:7000/auth/*`
- `/api/*` → `http://localhost:7000/api/*`

### State Management

Authentication state is managed using React Context API:
- `AuthContext` provides user state and auth functions
- `useAuth()` hook for accessing auth state in components
- Persistent storage using localStorage

## Testing the Application

### 1. Start Backend

```bash
# From project root
./start_backend.sh
```

Make sure the backend is running and seeded with test data:

```bash
cd backend
python seed_data.py
```

### 2. Start Frontend

```bash
# From project root
./start_frontend.sh
```

### 3. Test Login

1. Navigate to http://localhost:5173
2. You'll be redirected to the login page
3. Try logging in with different roles:

**Test Admin Role:**
- Email: `admin@dealflow.com`
- Password: `admin123`
- Expected: See Admin tag (red) with full permissions

**Test Analyst Role:**
- Email: `analyst@dealflow.com`
- Password: `analyst123`
- Expected: See Analyst tag (blue) with deal/memo permissions

**Test Partner Role:**
- Email: `partner@dealflow.com`
- Password: `partner123`
- Expected: See Partner tag (green) with comment/vote permissions

### 4. Test Features

- ✅ Login with valid credentials
- ✅ See error message with invalid credentials
- ✅ View user information on dashboard
- ✅ See role-specific capabilities
- ✅ Logout and redirect to login
- ✅ Try accessing dashboard without login (should redirect)
- ✅ Try accessing login when already logged in (should redirect)

## Troubleshooting

### Backend Not Connecting

**Problem**: Cannot connect to backend API

**Solution**:
1. Verify backend is running on port 7000
2. Check `vite.config.ts` proxy settings
3. Look for CORS errors in browser console

### Token Expired

**Problem**: Getting 401 Unauthorized errors

**Solution**:
1. Logout and login again
2. Check if backend is running
3. Clear localStorage: `localStorage.clear()`

### Dependencies Issues

**Problem**: Module not found errors

**Solution**:
```bash
cd frontend/UI
rm -rf node_modules package-lock.json
npm install
```

### Port Already in Use

**Problem**: Port 5173 is already in use

**Solution**:
```bash
# Kill process on port 5173
lsof -ti:5173 | xargs kill -9

# Or change port in vite.config.ts
```

## Development Commands

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type check
npx tsc --noEmit
```

## Next Steps

The authentication foundation is now complete! Future enhancements could include:

- 📊 Deal pipeline Kanban board
- 📝 IC memo creation and editing
- 💬 Comments system
- 🗳️ Voting functionality
- 📈 Activity feed
- 👥 User management (Admin)
- 🔍 Search and filtering
- 📱 Mobile responsive improvements

## Support

If you encounter any issues:

1. Check the browser console for errors
2. Verify backend is running and accessible
3. Check network tab for API call failures
4. Review the README.md for additional information

