import sys
from pathlib import Path
import threading
import uvicorn
import asyncio

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# настройка джанго орм перед импортом моделей
from orm_setup import setup_orm
setup_orm()

# импорты после настройки орм
from config import get_bot_token
from bot import get_application
from web import app as fastapi_app


# фастапи запускается в отдельном потоке
def run_fastapi():
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000, log_level="info")

# бот запускается
def run_bot():
    token = get_bot_token()
    app = get_application(token)
    print("Бот запущен. Нажми Ctrl+C для остановки.")
    app.run_polling()  # синхронный запуск


if __name__ == "__main__":
    web_thread = threading.Thread(target=run_fastapi, daemon=True)
    web_thread.start()
    try:
        run_bot()
    except KeyboardInterrupt:
        print("\nБот остановлен")
        sys.exit(0)