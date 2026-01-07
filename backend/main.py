"""
FastAPI main application with Django ORM integration
"""
import sys
from pathlib import Path

# Add backend to Python path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import setup_django

# Setup Django
setup_django()

# Import routers (will be created next)
from api import auth, deals, memos, interactions, users

# Create FastAPI app
app = FastAPI(
    title="Deal Pipeline API",
    description="Investment deal pipeline management system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(deals.router, prefix="/api/deals", tags=["Deals"])
app.include_router(memos.router, prefix="/api/deals", tags=["IC Memos"])
app.include_router(interactions.router, prefix="/api/deals", tags=["Interactions"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])


@app.get("/")
async def root():
    return {
        "message": "Deal Pipeline API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

