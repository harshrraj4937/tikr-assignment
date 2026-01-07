# Tikr Frontend - Investment Deal Pipeline

A modern React frontend built with Vite, TypeScript, and Ant Design for the Tikr investment deal pipeline management system.

## Features

- 🔐 **Authentication**: Email/password login with JWT tokens
- 👥 **Role-Based Access**: Support for Admin, Analyst, and Partner roles
- 🎨 **Modern UI**: Beautiful interface using Ant Design components
- ⚡ **Fast Development**: Powered by Vite for lightning-fast HMR
- 🔒 **Protected Routes**: Automatic redirection based on authentication status

## Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Ant Design 5** - UI component library
- **Axios** - HTTP client
- **React Router 6** - Routing

## Getting Started

### Prerequisites

- Node.js 16+ and npm
- Backend API running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install
```

### Development

```bash
# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

### Build for Production

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
src/
├── components/         # Reusable components
│   └── ProtectedRoute.tsx
├── contexts/          # React contexts
│   └── AuthContext.tsx
├── pages/             # Page components
│   ├── Login.tsx
│   └── Dashboard.tsx
├── services/          # API services
│   └── api.ts
├── types/             # TypeScript types
│   └── auth.ts
├── App.tsx            # Main app component
├── main.tsx           # App entry point
└── index.css          # Global styles
```

## Authentication Flow

1. User enters email and password on the login page
2. Credentials are sent to `/auth/login` endpoint
3. On success, JWT token and user data are stored in localStorage
4. User is redirected to the dashboard
5. Protected routes check authentication status
6. Token is automatically included in all API requests

## User Roles

### Admin (Hierarchy Level 3)
- Manage users and assign roles
- Full access to all deals and IC memos
- Can perform all actions in the system

### Analyst (Hierarchy Level 2)
- Create and edit deals
- Create and edit IC memos
- Move deals through pipeline stages

### Partner (Hierarchy Level 1)
- View deals and IC memos
- Comment on deals
- Vote to approve or decline deals

## API Integration

The frontend connects to these backend endpoints:

- `POST /auth/login` - User authentication
- `GET /auth/me` - Get current user information

All authenticated requests include the JWT token in the Authorization header.

## Environment

The app is configured to proxy API requests to `http://localhost:8000` in development mode. This is configured in `vite.config.ts`.

## Available Pages

- `/login` - Login page (redirects to dashboard if already authenticated)
- `/dashboard` - User dashboard showing profile and role information
- `/` - Redirects to dashboard

## Testing Users

Use the backend's seeded data to test with different roles:

- Admin user
- Analyst user  
- Partner user

(Refer to backend documentation for credentials)

## Troubleshooting

### Backend Connection Issues

Make sure the backend is running on `http://localhost:8000`. Check the proxy configuration in `vite.config.ts` if using a different port.

### Token Expiration

If you get 401 errors, your token may have expired. Log out and log in again.

### Build Errors

Clear the node_modules and reinstall:

```bash
rm -rf node_modules package-lock.json
npm install
```

## Future Enhancements

- Deal pipeline Kanban board
- IC memo creation and editing
- Comments and voting functionality
- Activity feed
- User management (Admin only)

