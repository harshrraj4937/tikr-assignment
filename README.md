# Deal Pipeline - Investment Deal Management System

A full-stack web application for managing investment deals through a pipeline, built with FastAPI + Django ORM (backend) and React + Ant Design (frontend).

## Features

### 1. Authentication & Role-Based Access Control
- Email/password authentication with JWT tokens
- Three roles with different permissions:
  - **Admin**: Full system access, can manage users
  - **Analyst**: Create/edit deals and IC memos
  - **Partner**: Comment, vote, and approve/decline deals

### 2. Deal Pipeline (Kanban Board)
- Visual Kanban board with 6 stages: Sourced → Screen → Diligence → IC → Invested → Passed
- Drag-and-drop interface to move deals between stages
- Deal fields: name, company_url, owner, stage, round, check_size, status
- Automatic activity logging on stage changes

### 3. IC Memo (Investment Committee Memo)
- Structured editor with 6 fixed sections: Summary, Market, Product, Traction, Risks, Open Questions
- Full versioning: each save creates a new version with complete snapshot
- Version history viewer to review older versions (read-only)
- Markdown support for formatting

### 4. Collaboration Features
- **Comments**: All users can comment on deals
- **Voting**: Partners and Admins can vote to approve/decline deals
- **Activity Feed**: Complete timeline of all deal changes

### 5. User Management
- Admin-only interface to create and manage users
- Assign roles to users

## Tech Stack

### Backend
- **FastAPI**: Modern web framework for building APIs
- **Django ORM**: Database models and migrations
- **PostgreSQL/SQLite**: Database (SQLite for development)
- **JWT**: Token-based authentication
- **Pydantic**: Data validation

### Frontend
- **React 18**: UI library
- **TypeScript**: Type-safe JavaScript
- **Ant Design**: UI component library
- **@dnd-kit**: Drag-and-drop functionality
- **Axios**: HTTP client
- **React Router**: Navigation
- **React Markdown**: Markdown rendering

## Project Structure

```
tikr/
├── backend/
│   ├── api/          # FastAPI route handlers
│   │   ├── auth.py        # Authentication endpoints
│   │   ├── deals.py       # Deal CRUD and stage management
│   │   ├── memos.py       # IC Memo versioning
│   │   ├── interactions.py # Comments and votes
│   │   └── users.py       # User management (Admin)
│   ├── models/       # Django ORM models
│   │   └── models.py      # All database models
│   ├── core/         # Core utilities
│   │   ├── auth.py        # JWT authentication
│   │   ├── permissions.py # Permission checking
│   │   ├── schemas.py     # Pydantic schemas
│   │   ├── settings.py    # Django settings
│   │   └── database.py    # Database setup
│   ├── main.py       # FastAPI application entry point
│   ├── manage.py     # Django management script
│   ├── seed_data.py  # Database seeding script
│   └── requirements.txt
├── frontend/
│   ├── UI/           # React application
│   │   └── src/
│   │       ├── pages/          # Page components
│   │       ├── components/     # Reusable components
│   │       └── App.tsx         # Main app with routing
│   ├── services/     # API client services
│   │   ├── api.ts          # Axios instance with JWT
│   │   ├── authService.ts
│   │   ├── dealService.ts
│   │   ├── memoService.ts
│   │   ├── interactionService.ts
│   │   └── userService.ts
│   ├── utils/        # Utilities and types
│   │   ├── types.ts        # TypeScript interfaces
│   │   └── constants.ts    # App constants
│   └── components/   # Shared components
└── README.md

```

## Setup Instructions

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Django migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Seed the database with test data**:
   ```bash
   python seed_data.py
   ```
   This creates 3 roles and 3 test users:
   - Admin: `admin@dealflow.com` / `admin123`
   - Analyst: `analyst@dealflow.com` / `analyst123`
   - Partner: `partner@dealflow.com` / `partner123`

5. **Start the backend server**:
   ```bash
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 7000
   ```
   Backend will be available at `http://localhost:7000`
   API docs at `http://localhost:7000/docs`

### Frontend Setup

1. **Navigate to frontend UI directory**:
   ```bash
   cd frontend/UI
   ```

2. **Install Node dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```
   Frontend will be available at `http://localhost:5173`

## Usage

### Test Accounts

The application comes with three pre-configured test accounts:

1. **Admin Account**
   - Email: `admin@dealflow.com`
   - Password: `admin123`
   - Permissions: Full access, can manage users

2. **Analyst Account**
   - Email: `analyst@dealflow.com`
   - Password: `analyst123`
   - Permissions: Create/edit deals and IC memos

3. **Partner Account**
   - Email: `partner@dealflow.com`
   - Password: `partner123`
   - Permissions: Comment, vote, and approve/decline deals

### Workflow Example

1. **Login as Analyst** and create a new deal
2. **Drag the deal** through stages (Sourced → Screen → Diligence)
3. **Create an IC Memo** with detailed analysis
4. **Add comments** to discuss the deal
5. **Login as Partner** and vote to approve/decline
6. **Move to final stage** based on decision
7. **Login as Admin** to manage users and view all activities

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login with email/password
- `GET /api/auth/me` - Get current user
- `POST /api/auth/register` - Register new user (Admin only)

### Deals
- `GET /api/deals` - List all active deals
- `POST /api/deals` - Create new deal (Analyst+)
- `GET /api/deals/{id}` - Get deal details
- `PATCH /api/deals/{id}` - Update deal (owner or Admin)
- `PATCH /api/deals/{id}/stage` - Move deal to different stage
- `DELETE /api/deals/{id}` - Archive deal (Admin)
- `GET /api/deals/{id}/activities` - Get activity log

### IC Memos
- `GET /api/deals/{deal_id}/memos` - List all memo versions
- `POST /api/deals/{deal_id}/memos` - Save new memo version (Analyst+)
- `GET /api/deals/{deal_id}/memos/{version}` - Get specific version
- `GET /api/deals/{deal_id}/memos/latest` - Get latest version

### Interactions
- `GET /api/deals/{deal_id}/comments` - List comments
- `POST /api/deals/{deal_id}/comments` - Add comment
- `GET /api/deals/{deal_id}/votes` - List votes
- `POST /api/deals/{deal_id}/vote` - Cast vote (Partner+)
- `GET /api/deals/{deal_id}/vote/summary` - Get vote summary

### Users
- `GET /api/users` - List users (Admin only)
- `POST /api/users` - Create user (Admin only)
- `PATCH /api/users/{id}` - Update user (Admin only)
- `GET /api/users/roles` - List all roles

## Key Implementation Details

### Deal Stage Changes
- Drag-and-drop calls `PATCH /deals/{id}/stage` with new stage
- Backend creates Activity record before updating Deal
- Activity text: `"{user.name} moved {deal.name} from {old_stage} to {new_stage}"`

### IC Memo Versioning
- Every save creates new ICMemo row with incremented version
- Stores full snapshot of all 6 sections as JSON
- Version list shows created_at and created_by
- Click version to view in read-only modal

### Activity Logging
- Automatically logs: stage changes, deal creation, memo saves
- Displays in timeline on deal detail page

### Role-Based Permissions

| Action | Admin | Analyst | Partner |
|--------|-------|---------|---------|
| View all deals | ✓ | ✓ | ✓ |
| Create deal | ✓ | ✓ | ✗ |
| Edit own deal | ✓ | ✓ | ✗ |
| Edit any deal | ✓ | ✗ | ✗ |
| Create/edit memo | ✓ | ✓ | ✗ |
| Comment | ✓ | ✓ | ✓ |
| Vote | ✓ | ✗ | ✓ |
| Manage users | ✓ | ✗ | ✗ |

## Development

### Running Tests
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend/UI
npm test
```

### Database Migrations
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

### Access Django Admin
```bash
python manage.py createsuperuser
# Then visit http://localhost:7000/admin
```

## Production Considerations

1. **Environment Variables**: Move sensitive config to environment variables
2. **Database**: Use PostgreSQL instead of SQLite
3. **CORS**: Configure CORS properly for production domains
4. **JWT Secret**: Generate and use a secure random secret key
5. **HTTPS**: Enable HTTPS for production
6. **Error Handling**: Add comprehensive error handling and logging
7. **Rate Limiting**: Implement rate limiting on API endpoints
8. **File Uploads**: If adding file uploads, configure proper storage

## License

MIT License

## Author

Built as a take-home assignment for investment team deal management.

