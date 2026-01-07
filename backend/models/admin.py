"""Django admin configuration for models"""
from django.contrib import admin
from .models import User, Role, Deal, ICMemo, Activity, Comment, Vote


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'hierarchy_level', 'is_active', 'created_on']
    list_filter = ['is_active']
    search_fields = ['name']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active']
    search_fields = ['email', 'username']


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'stage', 'status', 'check_size', 'created_at']
    list_filter = ['stage', 'status']
    search_fields = ['name', 'owner__email']


@admin.register(ICMemo)
class ICMemoAdmin(admin.ModelAdmin):
    list_display = ['deal', 'version', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['deal__name', 'created_by__email']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['deal', 'user', 'action', 'created_at']
    list_filter = ['created_at']
    search_fields = ['deal__name', 'user__email', 'action']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['deal', 'user', 'content', 'created_at']
    list_filter = ['created_at']
    search_fields = ['deal__name', 'user__email', 'content']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['deal', 'user', 'vote', 'created_at']
    list_filter = ['vote', 'created_at']
    search_fields = ['deal__name', 'user__email']
