"""Django app configuration for models"""
from django.apps import AppConfig


class ModelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'models'
    label = 'models'
    
    def ready(self):
        """Import models when app is ready"""
        from . import models  # noqa

