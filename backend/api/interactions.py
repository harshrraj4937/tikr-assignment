"""Comments and Votes API routes"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from core.schemas import CommentResponse, CommentCreate, VoteResponse, VoteCreate
from core.auth import get_current_user
from core.permissions import can_vote
from models.models import User, Deal, Comment, Vote

router = APIRouter()


# Comment endpoints
@router.get("/{deal_id}/comments", response_model=List[CommentResponse])
def list_comments(
    deal_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    List all comments for a deal
    """
    try:
        deal = Deal.objects.get(id=deal_id)
    except Deal.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deal not found"
        )
    
    comments = Comment.objects.select_related('user', 'user__role').filter(deal=deal).order_by('-created_at').all()
    return [CommentResponse.model_validate(comment) for comment in comments]


@router.post("/{deal_id}/comments", response_model=CommentResponse)
def create_comment(
    deal_id: int,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Add a comment to a deal (all roles can comment)
    """
    try:
        deal = Deal.objects.get(id=deal_id)
    except Deal.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deal not found"
        )
    
    # Create comment
    comment = Comment.objects.create(
        deal=deal,
        user=current_user,
        content=comment_data.content
    )
    
    # Reload to get related objects
    comment = Comment.objects.select_related('user', 'user__role').get(id=comment.id)
    
    return CommentResponse.model_validate(comment)


# Vote endpoints
@router.get("/{deal_id}/votes", response_model=List[VoteResponse])
def list_votes(
    deal_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    List all votes for a deal
    """
    try:
        deal = Deal.objects.get(id=deal_id)
    except Deal.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deal not found"
        )
    
    votes = Vote.objects.select_related('user', 'user__role').filter(deal=deal).order_by('-created_at').all()
    return [VoteResponse.model_validate(vote) for vote in votes]


@router.post("/{deal_id}/vote", response_model=VoteResponse)
def cast_vote(
    deal_id: int,
    vote_data: VoteCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Vote on a deal (Partners and Admins only)
    """
    if not can_vote(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Partners and Admins can vote"
        )
    
    try:
        deal = Deal.objects.get(id=deal_id)
    except Deal.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deal not found"
        )
    
    # Validate vote value
    if vote_data.vote not in ['approve', 'decline']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vote must be either 'approve' or 'decline'"
        )
    
    # Check if user has already voted
    existing_vote = Vote.objects.filter(deal=deal, user=current_user).first()
    
    if existing_vote:
        # Update existing vote
        existing_vote.vote = vote_data.vote
        existing_vote.comment = vote_data.comment
        existing_vote.save()
        vote = existing_vote
    else:
        # Create new vote
        vote = Vote.objects.create(
            deal=deal,
            user=current_user,
            vote=vote_data.vote,
            comment=vote_data.comment
        )
    
    # Reload to get related objects
    vote = Vote.objects.select_related('user', 'user__role').get(id=vote.id)
    
    return VoteResponse.model_validate(vote)


@router.get("/{deal_id}/vote/summary")
def get_vote_summary(
    deal_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    Get vote summary for a deal
    """
    try:
        deal = Deal.objects.get(id=deal_id)
    except Deal.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deal not found"
        )
    
    votes = Vote.objects.filter(deal=deal)
    
    approve_count = votes.filter(vote='approve').count()
    decline_count = votes.filter(vote='decline').count()
    total_votes = votes.count()
    
    return {
        "total_votes": total_votes,
        "approve": approve_count,
        "decline": decline_count
    }

