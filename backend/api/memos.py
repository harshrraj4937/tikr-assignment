"""IC Memo API routes with versioning"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from core.schemas import ICMemoResponse, ICMemoCreate
from core.auth import get_current_user
from core.permissions import is_analyst_or_above
from models.models import User, Deal, ICMemo, Activity

router = APIRouter()


@router.get("/{deal_id}/memos", response_model=List[ICMemoResponse])
def list_memo_versions(
    deal_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    List all IC Memo versions for a deal
    """
    try:
        deal = Deal.objects.get(id=deal_id)
    except Deal.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deal not found"
        )
    
    memos = ICMemo.objects.select_related('created_by', 'created_by__role').filter(deal=deal).order_by('-version').all()
    return [ICMemoResponse.model_validate(memo) for memo in memos]


@router.post("/{deal_id}/memos", response_model=ICMemoResponse)
def create_memo_version(
    deal_id: int,
    memo_data: ICMemoCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Create a new IC Memo version (Analyst and Admin only)
    Each save creates a new version with full snapshot
    """
    if not is_analyst_or_above(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Analysts and Admins can create/edit memos"
        )
    
    try:
        deal = Deal.objects.get(id=deal_id)
    except Deal.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deal not found"
        )
    
    # Create new memo version (version auto-increments in save method)
    memo = ICMemo.objects.create(
        deal=deal,
        sections=memo_data.sections.model_dump(),
        created_by=current_user
    )
    
    # Log activity
    Activity.objects.create(
        deal=deal,
        user=current_user,
        action=f"saved IC Memo version {memo.version}"
    )
    
    # Reload to get related objects
    memo = ICMemo.objects.select_related('created_by', 'created_by__role').get(id=memo.id)
    
    return ICMemoResponse.model_validate(memo)


@router.get("/{deal_id}/memos/{version}", response_model=ICMemoResponse)
def get_memo_version(
    deal_id: int,
    version: int,
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific IC Memo version
    """
    try:
        deal = Deal.objects.get(id=deal_id)
    except Deal.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deal not found"
        )
    
    try:
        memo = ICMemo.objects.select_related('created_by', 'created_by__role').get(deal=deal, version=version)
    except ICMemo.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Memo version {version} not found"
        )
    
    return ICMemoResponse.model_validate(memo)


@router.get("/{deal_id}/memos/latest", response_model=ICMemoResponse)
def get_latest_memo(
    deal_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    Get the latest IC Memo version for a deal
    """
    try:
        deal = Deal.objects.get(id=deal_id)
    except Deal.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deal not found"
        )
    
    memo = ICMemo.objects.select_related('created_by', 'created_by__role').filter(deal=deal).order_by('-version').first()
    
    if not memo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No memos found for this deal"
        )
    
    return ICMemoResponse.model_validate(memo)

