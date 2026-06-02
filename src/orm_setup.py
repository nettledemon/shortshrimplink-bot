import os
import django
from django.conf import settings as django_settings
from django.apps import apps


def setup_orm():
    # енв с настройками
    if not os.environ.get('DJANGO_SETTINGS_MODULE'):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.db_settings')

    # конфиг
    if not django_settings.configured:
        import db_settings as app_settings

        config = {
            key: value for key, value in app_settings.__dict__.items()
            if key.isupper()
        }

        django_settings.configure(**config)

    if not apps.apps_ready:
        django.setup()