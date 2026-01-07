"""User management API routes (Admin only)"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from core.schemas import UserResponse, UserCreate, UserUpdate
from core.auth import get_current_user
from models.models import User, Role

router = APIRouter()


@router.get("", response_model=List[UserResponse])
def list_users(current_user: User = Depends(get_current_user)):
    """
    List all users (Admin only)
    """
    if not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can list users"
        )
    
    users = User.objects.select_related('role').all()
    return [UserResponse.model_validate(user) for user in users]


@router.post("", response_model=UserResponse)
def create_user(
    user_data: UserCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Create a new user (Admin only)
    """
    if not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create users"
        )
    
    # Check if email already exists
    if User.objects.filter(email=user_data.email).exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    if User.objects.filter(username=user_data.username).exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Get role if provided
    role = None
    if user_data.role_id:
        try:
            role = Role.objects.get(id=user_data.role_id)
        except Role.DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
    
    # Create user
    user = User.objects.create(
        email=user_data.email,
        username=user_data.username,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=role
    )
    user.set_password(user_data.password)
    user.save()
    
    return UserResponse.model_validate(user)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Update a user (Admin only)
    """
    if not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update users"
        )
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update fields
    if user_data.first_name is not None:
        user.first_name = user_data.first_name
    if user_data.last_name is not None:
        user.last_name = user_data.last_name
    if user_data.role_id is not None:
        try:
            role = Role.objects.get(id=user_data.role_id)
            user.role = role
        except Role.DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
    
    user.save()
    
    return UserResponse.model_validate(user)


@router.get("/roles", response_model=List[dict])
def list_roles(current_user: User = Depends(get_current_user)):
    """
    List all available roles
    """
    roles = Role.objects.all()
    return [
        {
            "id": role.id,
            "name": role.name,
            "hierarchy_level": role.hierarchy_level,
            "description": role.description
        }
        for role in roles
    ]

