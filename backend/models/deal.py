"""Deal model for investment pipeline"""
from django.db import models
from django.utils import timezone


class Deal(models.Model):
    """
    Deal model representing an investment opportunity in the pipeline
    """
    STAGE_CHOICES = [
        ('Sourced', 'Sourced'),
        ('Screen', 'Screen'),
        ('Diligence', 'Diligence'),
        ('IC', 'IC'),
        ('Invested', 'Invested'),
        ('Passed', 'Passed'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]
    
    name = models.CharField(max_length=255)
    company_url = models.URLField(blank=True, null=True)
    owner = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='owned_deals'
    )
    stage = models.CharField(
        max_length=20,
        choices=STAGE_CHOICES,
        default='Sourced'
    )
    round = models.CharField(max_length=100, blank=True, null=True)
    check_size = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Deal"
        verbose_name_plural = "Deals"
        ordering = ['-created_at']
        app_label = 'models'

    def __str__(self):
        return f"{self.name} - {self.stage}"

