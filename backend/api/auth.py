"""Authentication API routes"""
from fastapi import APIRouter, HTTPException, status, Depends
from core.schemas import LoginRequest, TokenResponse, RegisterRequest, UserResponse
from core.auth import create_access_token, get_current_user, get_password_hash
from models.models import User, Role

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest):
    """
    Login with email and password
    Returns JWT token
    """
    try:
        user = User.objects.select_related('role').get(email=credentials.email)
    except User.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not user.check_password(credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Create JWT token
    access_token = create_access_token(data={"user_id": user.id, "email": user.email})
    
    # Convert user to response model
    user_response = UserResponse.model_validate(user)
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )


@router.post("/register", response_model=UserResponse)
def register(
    user_data: RegisterRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Register a new user (Admin only)
    """
    # Check if current user is Admin
    if not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create new users"
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
    
    # Get role
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


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current user information
    """
    return UserResponse.model_validate(current_user)

