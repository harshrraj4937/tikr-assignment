"""Seed script to create initial roles and users"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from models.models import Role, User


def seed_roles():
    """Create initial roles"""
    roles_data = [
        {
            'name': 'Admin',
            'hierarchy_level': 3,
            'description': 'Full system access, can manage users',
            'permissions': [
                'view_deals', 'create_deals', 'edit_any_deal', 'delete_deals',
                'create_memos', 'edit_memos', 'comment', 'vote', 'manage_users'
            ]
        },
        {
            'name': 'Analyst',
            'hierarchy_level': 2,
            'description': 'Can create and edit deals and IC memos',
            'permissions': [
                'view_deals', 'create_deals', 'edit_own_deal',
                'create_memos', 'edit_memos', 'comment'
            ]
        },
        {
            'name': 'Partner',
            'hierarchy_level': 1,
            'description': 'Can comment, vote, and approve/decline deals',
            'permissions': [
                'view_deals', 'comment', 'vote'
            ]
        }
    ]
    
    for role_data in roles_data:
        role, created = Role.objects.get_or_create(
            name=role_data['name'],
            defaults=role_data
        )
        if created:
            print(f"✓ Created role: {role.name}")
        else:
            print(f"  Role already exists: {role.name}")


def seed_users():
    """Create test users"""
    users_data = [
        {
            'email': 'admin@dealflow.com',
            'username': 'admin',
            'first_name': 'Admin',
            'last_name': 'User',
            'role_name': 'Admin',
            'password': 'admin123'
        },
        {
            'email': 'analyst@dealflow.com',
            'username': 'analyst',
            'first_name': 'Alice',
            'last_name': 'Analyst',
            'role_name': 'Analyst',
            'password': 'analyst123'
        },
        {
            'email': 'partner@dealflow.com',
            'username': 'partner',
            'first_name': 'Paul',
            'last_name': 'Partner',
            'role_name': 'Partner',
            'password': 'partner123'
        }
    ]
    
    for user_data in users_data:
        role = Role.objects.get(name=user_data['role_name'])
        password = user_data.pop('password')
        user_data.pop('role_name')
        
        user, created = User.objects.get_or_create(
            email=user_data['email'],
            defaults={**user_data, 'role': role}
        )
        
        if created:
            user.set_password(password)
            user.save()
            print(f"✓ Created user: {user.email} (password: {password})")
        else:
            print(f"  User already exists: {user.email}")


if __name__ == '__main__':
    print("Seeding database...")
    print("\n1. Creating roles:")
    seed_roles()
    
    print("\n2. Creating test users:")
    seed_users()
    
    print("\n✅ Database seeded successfully!")
    print("\nTest accounts:")
    print("  Admin:   admin@dealflow.com / admin123")
    print("  Analyst: analyst@dealflow.com / analyst123")
    print("  Partner: partner@dealflow.com / partner123")

