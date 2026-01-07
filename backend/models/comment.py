"""Comment model for deal discussions"""
from django.db import models
from django.utils import timezone


class Comment(models.Model):
    """
    Comments on deals for collaboration.
    All roles can comment.
    """
    deal = models.ForeignKey(
        'Deal',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['-created_at']
        app_label = 'models'

    def __str__(self):
        return f"{self.user.email} on {self.deal.name}"

