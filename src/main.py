import sys
import os

# чтобы видеть src
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# настройка джанго орм перед импортом моделей
from orm_setup import setup_orm
setup_orm()

# импорты после настройки орм
from config import get_bot_token
from bot import get_application


def main():
    token = get_bot_token()
    app = get_application(token)
    print("Бот запущен. Нажми Ctrl+C для остановки.")
    app.run_polling()  # синхронный запуск


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nБот остановлен")
        sys.exit(0)