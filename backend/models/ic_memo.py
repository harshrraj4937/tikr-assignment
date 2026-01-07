"""IC Memo model for investment committee memos"""
from django.db import models
from django.utils import timezone


class ICMemo(models.Model):
    """
    IC Memo (Investment Committee Memo) with versioning.
    Each save creates a new version row with full snapshot.
    """
    deal = models.ForeignKey(
        'Deal',
        on_delete=models.CASCADE,
        related_name='ic_memos'
    )
    version = models.PositiveIntegerField(default=1)
    sections = models.JSONField(
        default=dict,
        help_text="JSON object with keys: summary, market, product, traction, risks, open_questions"
    )
    created_by = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='created_memos'
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "IC Memo"
        verbose_name_plural = "IC Memos"
        ordering = ['-created_at']
        unique_together = ['deal', 'version']
        app_label = 'models'

    def __str__(self):
        return f"{self.deal.name} - Memo v{self.version}"

    def save(self, *args, **kwargs):
        """Auto-increment version number for the deal"""
        if not self.pk:  # Only for new memos
            last_memo = ICMemo.objects.filter(deal=self.deal).order_by('-version').first()
            if last_memo:
                self.version = last_memo.version + 1
            else:
                self.version = 1
        super().save(*args, **kwargs)

