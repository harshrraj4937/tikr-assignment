"""Pydantic schemas for API request/response validation"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


# Auth Schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: 'UserResponse'


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role_id: int


# Role Schemas
class RoleResponse(BaseModel):
    id: int
    name: str
    hierarchy_level: int
    permissions: List[str]
    
    class Config:
        from_attributes = True


# User Schemas
class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[RoleResponse] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role_id: Optional[int] = None


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role_id: Optional[int] = None


# Deal Schemas
class DealCreate(BaseModel):
    name: str
    company_url: Optional[str] = None
    round: Optional[str] = None
    check_size: Optional[Decimal] = None


class DealUpdate(BaseModel):
    name: Optional[str] = None
    company_url: Optional[str] = None
    round: Optional[str] = None
    check_size: Optional[Decimal] = None


class DealStageUpdate(BaseModel):
    stage: str


class DealResponse(BaseModel):
    id: int
    name: str
    company_url: Optional[str] = None
    owner: UserResponse
    stage: str
    round: Optional[str] = None
    check_size: Optional[Decimal] = None
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# IC Memo Schemas
class ICMemoSections(BaseModel):
    summary: str = ""
    market: str = ""
    product: str = ""
    traction: str = ""
    risks: str = ""
    open_questions: str = ""


class ICMemoCreate(BaseModel):
    sections: ICMemoSections


class ICMemoResponse(BaseModel):
    id: int
    deal_id: int
    version: int
    sections: dict
    created_by: UserResponse
    created_at: datetime
    
    class Config:
        from_attributes = True


# Activity Schema
class ActivityResponse(BaseModel):
    id: int
    deal_id: int
    user: UserResponse
    action: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Comment Schemas
class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    deal_id: int
    user: UserResponse
    content: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Vote Schemas
class VoteCreate(BaseModel):
    vote: str  # 'approve' or 'decline'
    comment: Optional[str] = None


class VoteResponse(BaseModel):
    id: int
    deal_id: int
    user: UserResponse
    vote: str
    comment: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Update forward references
TokenResponse.model_rebuild()

