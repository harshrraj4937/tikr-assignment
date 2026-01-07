"""Role model for role-based access control"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Role(models.Model):
    """
    Role model defining access levels and permissions.
    Hierarchy: Admin (3) > Analyst (2) > Partner (1)
    """
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Analyst', 'Analyst'),
        ('Partner', 'Partner'),
    ]
    
    name = models.CharField(
        max_length=100,
        choices=ROLE_CHOICES,
        unique=True
    )
    description = models.TextField(blank=True, null=True)
    hierarchy_level = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Higher number = higher hierarchy (Admin=3, Analyst=2, Partner=1)"
    )
    permissions = models.JSONField(
        default=list,
        blank=True,
        help_text="List of permissions for this role"
    )
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        ordering = ['-hierarchy_level', 'name']
        app_label = 'models'

    def __str__(self):
        return self.name

