"""Custom User model with role-based access"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """
    Custom user model extending AbstractUser with role relationship
    """
    email = models.EmailField(unique=True)
    role = models.ForeignKey(
        'Role',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Make email the primary authentication field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        app_label = 'models'

    def __str__(self):
        return f"{self.email} ({self.role.name if self.role else 'No Role'})"

    def has_permission(self, permission: str) -> bool:
        """Check if user has a specific permission"""
        if not self.role:
            return False
        return permission in self.role.permissions

    def is_admin(self) -> bool:
        """Check if user is Admin"""
        return self.role and self.role.name == 'Admin'

    def is_analyst(self) -> bool:
        """Check if user is Analyst"""
        return self.role and self.role.name == 'Analyst'

    def is_partner(self) -> bool:
        """Check if user is Partner"""
        return self.role and self.role.name == 'Partner'

    def can_edit_deal(self, deal) -> bool:
        """Check if user can edit a deal"""
        if self.is_admin():
            return True
        if self.is_analyst() and deal.owner_id == self.id:
            return True
        return False

