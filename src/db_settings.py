import os
from pathlib import Path

# там лежит manage.py
BASE_DIR = Path(__file__).resolve().parent.parent

# ключ нужен для работы джанги (можно любой)
SECRET_KEY = 'django-insecure-xyz1234567890'

# постгре
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'shortshrimplink_db'),
        'USER': os.getenv('DB_USER', 'mac'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),  # или 'db' для докера
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# без этого миграции не увидят модели
INSTALLED_APPS = ['src']

# часовые пояса не нужны
USE_TZ = True