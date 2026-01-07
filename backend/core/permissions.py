"""Permission checking utilities and decorators"""
from functools import wraps
from fastapi import HTTPException, status
from typing import Callable


def require_role(*allowed_roles: str):
    """
    Decorator to require specific role(s) for an endpoint
    Usage: @require_role("Admin", "Analyst")
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, current_user=None, **kwargs):
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated"
                )
            
            if not current_user.role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User has no role assigned"
                )
            
            if current_user.role.name not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission denied. Required role: {', '.join(allowed_roles)}"
                )
            
            return await func(*args, current_user=current_user, **kwargs)
        
        return wrapper
    return decorator


def check_permission(user, permission: str) -> bool:
    """Check if user has a specific permission"""
    if not user or not user.role:
        return False
    return permission in user.role.permissions


def require_permission(permission: str):
    """
    Decorator to require a specific permission for an endpoint
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, current_user=None, **kwargs):
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated"
                )
            
            if not check_permission(current_user, permission):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission denied. Required permission: {permission}"
                )
            
            return await func(*args, current_user=current_user, **kwargs)
        
        return wrapper
    return decorator


def is_admin(user) -> bool:
    """Check if user is Admin"""
    return user and user.role and user.role.name == 'Admin'


def is_analyst_or_above(user) -> bool:
    """Check if user is Analyst or Admin"""
    return user and user.role and user.role.name in ['Admin', 'Analyst']


def is_partner_or_above(user) -> bool:
    """Check if user is Partner, Analyst, or Admin"""
    return user and user.role and user.role.name in ['Admin', 'Analyst', 'Partner']


def can_edit_deal(user, deal) -> bool:
    """Check if user can edit a specific deal"""
    if is_admin(user):
        return True
    if is_analyst_or_above(user) and deal.owner_id == user.id:
        return True
    return False


def can_vote(user) -> bool:
    """Check if user can vote on deals"""
    return user and user.role and user.role.name in ['Admin', 'Partner']

