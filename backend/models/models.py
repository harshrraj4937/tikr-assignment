"""All Django models for the Deal Pipeline application"""
from django.db import models
from django.contrib.auth.models import AbstractUser
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

    def __str__(self):
        return self.name


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

    def __str__(self):
        return f"{self.name} - {self.stage}"


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

    def __str__(self):
        return f"{self.user.email}: {self.action}"


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

    def __str__(self):
        return f"{self.user.email} on {self.deal.name}"


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

    def __str__(self):
        return f"{self.user.email} - {self.vote} on {self.deal.name}"

