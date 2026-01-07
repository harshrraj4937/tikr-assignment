"""
Database configuration for Django ORM with FastAPI
"""
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

if not settings.configured:
    django.setup()


def setup_django():
    """Initialize Django for use with FastAPI"""
    if not settings.configured:
        django.setup()

