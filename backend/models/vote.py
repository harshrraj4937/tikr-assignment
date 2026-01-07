"""Vote model for partner approvals"""
from django.db import models
from django.utils import timezone


class Vote(models.Model):
    """
    Votes for deals - Partners and Admins can vote to approve or decline
    """
    VOTE_CHOICES = [
        ('approve', 'Approve'),
        ('decline', 'Decline'),
    ]
    
    deal = models.ForeignKey(
        'Deal',
        on_delete=models.CASCADE,
        related_name='votes'
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='votes'
    )
    vote = models.CharField(
        max_length=10,
        choices=VOTE_CHOICES
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"
        ordering = ['-created_at']
        unique_together = ['deal', 'user']
        app_label = 'models'

    def __str__(self):
        return f"{self.user.email} - {self.vote} on {self.deal.name}"

