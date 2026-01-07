"""Activity model for tracking deal changes"""
from django.db import models
from django.utils import timezone


class Activity(models.Model):
    """
    Activity log for tracking changes to deals.
    Automatically created on stage changes, deal creation, memo saves, etc.
    """
    deal = models.ForeignKey(
        'Deal',
        on_delete=models.CASCADE,
        related_name='activities'
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='activities'
    )
    action = models.TextField(
        help_text="Description of the action (e.g., 'moved from Screen to Diligence')"
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
        ordering = ['-created_at']
        app_label = 'models'

    def __str__(self):
        return f"{self.user.email}: {self.action}"

