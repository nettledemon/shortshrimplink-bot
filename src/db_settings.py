from pathlib import Path


# там лежит manage.py
BASE_DIR = Path(__file__).resolve().parent.parent

# ключ нужен для работы джанги (можно любой)
SECRET_KEY = 'django-insecure-xyz1234567890'

# постгре
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shortshrimplink_db',  # имя базы данных
        'USER': 'mac',                 # пользователь
        'PASSWORD': '',                # пароль
        'HOST': 'localhost',           # или 'db', если в docker
        'PORT': '5432',
    }
}

# без этого миграции не увидят модели
INSTALLED_APPS = [
    'src',
]

# часовые пояса не нужны
USE_TZ = True