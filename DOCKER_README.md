# Docker Setup Guide for Tikr Application

This guide explains how to run the Tikr application using Docker.

## 📁 Docker Files Created

- `backend/Dockerfile` - Backend container configuration (FastAPI + Django ORM)
- `frontend/UI/Dockerfile` - Frontend container configuration (React + Vite)
- `docker-compose.yml` - Run both frontend and backend together
- `docker-compose.backend.yml` - Run backend only
- `docker-compose.frontend.yml` - Run frontend only
- `.dockerignore` files - Optimize Docker build context

## 🚀 Quick Start

### Option 1: Run Full Stack (Backend + Frontend)

```bash
# Build and start both services
docker compose up --build

# Or run in detached mode (background)
docker compose up -d --build

# View logs
docker compose logs -f

# Stop services
docker compose down
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Run Backend Only

```bash
# Build and start backend
docker compose -f docker-compose.backend.yml up --build

# Or in detached mode
docker compose -f docker-compose.backend.yml up -d --build

# Stop backend
docker compose -f docker-compose.backend.yml down
```

Backend will be available at http://localhost:8000

### Option 3: Run Frontend Only

```bash
# Build and start frontend
docker compose -f docker-compose.frontend.yml up --build

# Or in detached mode
docker compose -f docker-compose.frontend.yml up -d --build

# Stop frontend
docker compose -f docker-compose.frontend.yml down
```

Frontend will be available at http://localhost:5173

## 🔧 Useful Docker Commands

### View Running Containers
```bash
docker ps
```

### View Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
```

### Restart Services
```bash
# Restart all
docker compose restart

# Restart specific service
docker compose restart backend
docker compose restart frontend
```

### Execute Commands Inside Containers
```bash
# Backend shell
docker exec -it tikr-backend bash

# Run Django commands
docker exec -it tikr-backend python manage.py migrate
docker exec -it tikr-backend python manage.py shell

# Frontend shell
docker exec -it tikr-frontend sh
```

### Rebuild After Changes
```bash
# Rebuild all services
docker compose build --no-cache

# Rebuild specific service
docker compose build --no-cache backend
docker compose build --no-cache frontend
```

### Clean Up
```bash
# Stop and remove containers, networks
docker compose down

# Also remove volumes (⚠️ this will delete the database)
docker compose down -v

# Remove all unused Docker resources
docker system prune -a
```

## 🗄️ Database Management

The SQLite database is persisted in a Docker volume named `backend-db`. This means your data will survive container restarts.

### Run Migrations
```bash
docker exec -it tikr-backend python manage.py migrate
```

### Seed Database
```bash
# Copy seed script into container and run it
docker exec -it tikr-backend python seed_data.py
```

### Backup Database
```bash
# Copy database file from container
docker cp tikr-backend:/app/db.sqlite3 ./backup_db.sqlite3
```

### Restore Database
```bash
# Copy database file to container
docker cp ./backup_db.sqlite3 tikr-backend:/app/db.sqlite3
```

## 🔍 Troubleshooting

### Port Already in Use
If you get a "port already in use" error:

```bash
# Find process using the port
sudo lsof -i :8000  # For backend
sudo lsof -i :5173  # For frontend

# Kill the process
kill -9 <PID>
```

Or change the port in docker-compose.yml:
```yaml
ports:
  - "8001:8000"  # Use host port 8001 instead
```

### Container Won't Start
```bash
# Check logs for errors
docker compose logs backend
docker compose logs frontend

# Rebuild without cache
docker compose build --no-cache
docker compose up
```

### Database Issues
```bash
# Reset database (⚠️ this will delete all data)
docker compose down -v
docker compose up --build
```

### CORS Issues
The backend is configured to accept requests from localhost:5173. If you change the frontend port, update `backend/main.py`:

```python
allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:YOUR_PORT"],
```

## 🏗️ Development vs Production

### Development Mode
The current setup is optimized for development with:
- Hot-reloading enabled
- Debug mode on
- Volume mounts for live code changes

### Production Adjustments
For production, consider:

1. **Environment Variables**: Use `.env` files
2. **Database**: Switch to PostgreSQL
3. **Secrets**: Use Docker secrets or environment variables
4. **Nginx**: Add reverse proxy
5. **SSL**: Enable HTTPS
6. **Debug Mode**: Set `DEBUG=False`

## 📊 Resource Usage

You can monitor Docker resource usage:

```bash
# View resource usage
docker stats

# View disk usage
docker system df
```

## 🔐 Security Notes

⚠️ **Important for Production:**

1. Change `SECRET_KEY` and `JWT_SECRET_KEY` in settings
2. Set `DEBUG=False` in production
3. Use environment variables for sensitive data
4. Don't expose ports unnecessarily
5. Use proper authentication
6. Keep dependencies updated

## 📝 Environment Variables

Create a `.env` file for environment-specific configuration:

```env
# Backend
DEBUG=True
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret

# Frontend
VITE_API_URL=http://localhost:8000
```

Then update docker-compose.yml:
```yaml
env_file:
  - .env
```

## 🆘 Need Help?

- Check logs: `docker compose logs -f`
- Inspect container: `docker exec -it tikr-backend bash`
- Rebuild from scratch: `docker compose down -v && docker compose up --build`
- Check Docker documentation: https://docs.docker.com/

---

**Happy Dockerizing! 🐳**

