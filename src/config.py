import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


# токен бота
def get_bot_token() -> str:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN not set in .env")
    return token


# базовый адрес сервера
def get_base_url() -> str:
    base_url = os.getenv("BASE_URL")
    if not base_url:
        raise ValueError("BASE_URL not set in .env")
    return base_url


# сборка короткой ссылки
def get_full_short_url(short_code: str) -> str:
    return f"{get_base_url()}/{short_code}"