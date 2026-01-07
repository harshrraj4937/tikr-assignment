"""Deal management API routes"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from core.schemas import DealResponse, DealCreate, DealUpdate, DealStageUpdate, ActivityResponse
from core.auth import get_current_user
from core.permissions import is_analyst_or_above, can_edit_deal
from models.models import User, Deal, Activity

router = APIRouter()


@router.get("", response_model=List[DealResponse])
def list_deals(current_user: User = Depends(get_current_user)):
    """
    List all deals (accessible to all authenticated users)
    """
    deals = Deal.objects.select_related('owner', 'owner__role').filter(status='active').all()
    return [DealResponse.model_validate(deal) for deal in deals]


@router.post("", response_model=DealResponse)
def create_deal(
    deal_data: DealCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Create a new deal (Analyst and Admin only)
    """
    if not is_analyst_or_above(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Analysts and Admins can create deals"
        )
    
    # Create deal
    deal = Deal.objects.create(
        name=deal_data.name,
        company_url=deal_data.company_url,
        owner=current_user,
        round=deal_data.round,
        check_size=deal_data.check_size,
        stage='Sourced'
    )
    
    # Log activity
    Activity.objects.create(
        deal=deal,
        user=current_user,
        action=f"created deal '{deal.name}'"
    )
    
    # Reload to get related objects
    deal = Deal.objects.select_related('owner', 'owner__role').get(id=deal.id)
    
    return DealResponse.model_validate(deal)


@router.get("/{deal_id}", response_model=DealResponse)
def get_deal(
    deal_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific deal by ID
    """
    try:
        deal = Deal.objects.select_related('owner', 'owner__role').get(id=deal_id)
    except Deal.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deal not found"
        )
    
    return DealResponse.model_validate(deal)


@router.patch("/{deal_id}", response_model=DealResponse)
def update_deal(
    deal_id: int,
    deal_data: DealUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Update a deal (owner or Admin only)
    """
    try:
        deal = Deal.objects.select_related('owner').get(id=deal_id)
    except Deal.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deal not found"
        )
    
    # Check permissions
    if not can_edit_deal(current_user, deal):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to edit this deal"
        )
    
    # Update fields
    updated_fields = []
    if deal_data.name is not None:
        deal.name = deal_data.name
        updated_fields.append("name")
    if deal_data.company_url is not None:
        deal.company_url = deal_data.company_url
        updated_fields.append("company_url")
    if deal_data.round is not None:
        deal.round = deal_data.round
        updated_fields.append("round")
    if deal_data.check_size is not None:
        deal.check_size = deal_data.check_size
        updated_fields.append("check_size")
    
    deal.save()
    
    # Log activity if fields were updated
    if updated_fields:
        Activity.objects.create(
            deal=deal,
            user=current_user,
            action=f"updated {', '.join(updated_fields)}"
        )
    
    # Reload to get related objects
    deal = Deal.objects.select_related('owner', 'owner__role').get(id=deal.id)
    
    return DealResponse.model_validate(deal)


@router.patch("/{deal_id}/stage", response_model=DealResponse)
def update_deal_stage(
    deal_id: int,
    stage_data: DealStageUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Move a deal to a different stage (creates activity log)
    """
    try:
        deal = Deal.objects.select_related('owner').get(id=deal_id)
    except Deal.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deal not found"
        )
    
    # Validate stage
    valid_stages = ['Sourced', 'Screen', 'Diligence', 'IC', 'Invested', 'Passed']
    if stage_data.stage not in valid_stages:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid stage. Must be one of: {', '.join(valid_stages)}"
        )
    
    # Store old stage for activity log
    old_stage = deal.stage
    
    # Update stage
    deal.stage = stage_data.stage
    deal.save()
    
    # Log activity
    Activity.objects.create(
        deal=deal,
        user=current_user,
        action=f"moved '{deal.name}' from {old_stage} to {stage_data.stage}"
    )
    
    # Reload to get related objects
    deal = Deal.objects.select_related('owner', 'owner__role').get(id=deal.id)
    
    return DealResponse.model_validate(deal)


@router.delete("/{deal_id}")
def archive_deal(
    deal_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    Archive a deal (Admin only)
    """
    if not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can archive deals"
        )
    
    try:
        deal = Deal.objects.get(id=deal_id)
    except Deal.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deal not found"
        )
    
    # Archive instead of delete
    deal.status = 'archived'
    deal.save()
    
    # Log activity
    Activity.objects.create(
        deal=deal,
        user=current_user,
        action=f"archived deal '{deal.name}'"
    )
    
    return {"message": "Deal archived successfully"}


@router.get("/{deal_id}/activities", response_model=List[ActivityResponse])
def get_deal_activities(
    deal_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    Get activity log for a specific deal
    """
    try:
        deal = Deal.objects.get(id=deal_id)
    except Deal.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deal not found"
        )
    
    activities = Activity.objects.select_related('user', 'user__role').filter(deal=deal).all()
    return [ActivityResponse.model_validate(activity) for activity in activities]

