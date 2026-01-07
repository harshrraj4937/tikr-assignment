# Frontend Features Overview

## 🎨 UI/UX Design

### Color Scheme
- **Primary Color**: Purple gradient (#667eea to #764ba2)
- **Admin Role**: Red tag
- **Analyst Role**: Blue tag
- **Partner Role**: Green tag

### Design Philosophy
- Clean, modern interface
- Responsive and mobile-friendly
- Professional business application aesthetic
- Consistent spacing and typography
- Smooth transitions and loading states

## 📱 Pages

### 1. Login Page (`/login`)

**Layout:**
- Centered card on gradient background
- Logo/title: "Welcome to Tikr"
- Subtitle: "Investment Deal Pipeline Management"
- Email input field with validation
- Password input field
- Login button with loading state
- Error messages displayed inline

**Features:**
- Email format validation
- Required field validation
- Loading spinner during authentication
- Success/error messages using Ant Design notifications
- Auto-redirect to dashboard on success
- Auto-redirect away if already logged in

**Form Fields:**
- Email (required, must be valid email format)
- Password (required)

### 2. Dashboard Page (`/dashboard`)

**Layout:**
- Gradient background matching login
- Centered content card (max-width: 900px)
- User avatar and welcome message
- Logout button in header
- Two main sections:
  1. User Information Card
  2. Role & Permissions Card

**User Information Section:**
- User ID
- Email address
- Username
- First name (if available)
- Last name (if available)
- Account creation date (formatted)

**Role & Permissions Section:**
- Role name with color-coded tag and hierarchy level
- Hierarchy level number
- List of permissions (as tags)
- Role capabilities description box with:
  - **Admin**: Manage users, full access, all actions
  - **Analyst**: Create/edit deals, create/edit memos, move pipeline
  - **Partner**: View deals/memos, comment, vote

**Interactive Elements:**
- Logout button (red, with icon)
- Responsive layout for mobile devices

## 🔐 Authentication System

### Token Management
- JWT tokens stored in localStorage
- Automatic token inclusion in API headers
- Token validation on app load
- Automatic logout on token expiration (401 errors)

### Protected Routes
- Dashboard requires authentication
- Login page redirects if authenticated
- Loading states during auth checks
- Graceful error handling

### Security Features
- Passwords never stored locally
- Tokens cleared on logout
- Automatic redirect on unauthorized access
- HTTPS ready (for production)

## 🎯 User Roles

### Admin (Hierarchy Level 3)
**Tag Color:** Red

**Permissions:**
- view_deals
- create_deals
- edit_any_deal
- delete_deals
- create_memos
- edit_memos
- comment
- vote
- manage_users

**Capabilities:**
- Manage users and assign roles
- Full access to all deals and IC memos
- Can perform all actions in the system

### Analyst (Hierarchy Level 2)
**Tag Color:** Blue

**Permissions:**
- view_deals
- create_deals
- edit_own_deal
- create_memos
- edit_memos
- comment

**Capabilities:**
- Create and edit deals
- Create and edit IC memos
- Move deals through pipeline stages

### Partner (Hierarchy Level 1)
**Tag Color:** Green

**Permissions:**
- view_deals
- comment
- vote

**Capabilities:**
- View deals and IC memos
- Comment on deals
- Vote to approve or decline deals

## 🛠️ Technical Features

### React Components
- Functional components with hooks
- TypeScript for type safety
- Reusable component architecture
- Context API for state management

### Ant Design Integration
- Form components with validation
- Card layouts
- Descriptions for data display
- Tags for role/permission display
- Buttons with loading states
- Message notifications
- Spin loaders
- Icons from @ant-design/icons

### Routing
- React Router v6
- Protected route wrapper component
- Automatic redirects based on auth state
- Fallback routes (404 → dashboard)

### API Integration
- Axios for HTTP requests
- Request interceptors for auth tokens
- Response interceptors for error handling
- Centralized API service layer
- Type-safe API calls

### State Management
- AuthContext for global auth state
- useAuth hook for component access
- localStorage for persistence
- Loading states for async operations

### Developer Experience
- TypeScript for type safety
- Vite for fast development
- Hot module replacement (HMR)
- ESLint ready
- Clean project structure

## 📊 Data Flow

```
User Input (Login Form)
    ↓
API Call (POST /auth/login)
    ↓
Backend Validation
    ↓
JWT Token + User Data
    ↓
localStorage Storage
    ↓
AuthContext Update
    ↓
Dashboard Display
```

## 🔄 State Lifecycle

### On App Load
1. Check localStorage for token
2. If token exists, validate with backend
3. Update auth context with user data
4. Redirect based on auth state

### On Login
1. Submit credentials to backend
2. Receive token and user data
3. Store in localStorage
4. Update auth context
5. Redirect to dashboard

### On Logout
1. Clear localStorage
2. Reset auth context
3. Redirect to login page

### On Token Expiration
1. API returns 401 error
2. Interceptor catches error
3. Clear localStorage
4. Redirect to login page

## 🎨 Visual Hierarchy

### Login Page
```
┌─────────────────────────────────────┐
│     Gradient Background (Purple)    │
│                                      │
│   ┌───────────────────────────┐    │
│   │  Welcome to Tikr          │    │
│   │  Investment Deal Pipeline │    │
│   │                           │    │
│   │  [Email Input]            │    │
│   │  [Password Input]         │    │
│   │  [Login Button]           │    │
│   └───────────────────────────┘    │
│                                      │
└─────────────────────────────────────┘
```

### Dashboard Page
```
┌─────────────────────────────────────┐
│     Gradient Background (Purple)    │
│                                      │
│   ┌───────────────────────────┐    │
│   │ [Avatar] Welcome, Name!   │    │
│   │                  [Logout] │    │
│   ├───────────────────────────┤    │
│   │ User Information          │    │
│   │ • ID: 1                   │    │
│   │ • Email: user@email.com   │    │
│   │ • Username: username      │    │
│   │ • Created: Jan 1, 2024    │    │
│   ├───────────────────────────┤    │
│   │ Role & Permissions        │    │
│   │ • Role: [Admin] Level 3   │    │
│   │ • Permissions: [tags...]  │    │
│   │ • Capabilities:           │    │
│   │   - Manage users          │    │
│   │   - Full access           │    │
│   └───────────────────────────┘    │
│                                      │
└─────────────────────────────────────┘
```

## 🚀 Performance

- Fast initial load with Vite
- Code splitting ready
- Optimized bundle size
- Lazy loading for routes (ready for expansion)
- Efficient re-renders with React hooks

## ♿ Accessibility

- Semantic HTML
- ARIA labels on form inputs
- Keyboard navigation support
- Focus management
- Screen reader friendly

## 📱 Responsive Design

- Mobile-first approach
- Flexible layouts
- Responsive card widths
- Touch-friendly buttons
- Adaptive spacing

## 🧪 Testing Ready

- Component structure for unit tests
- API mocking support
- Type safety for test confidence
- Clear separation of concerns

