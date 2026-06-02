from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from database import save_link, link_exists, get_short_code_by_long_url
from utils import generate_short_code
from config import get_full_short_url


# команда чата /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"""Бот работает!
Список доступных команд:
/start - запустить бота (уже активно)
/shorten - укоротить ссылку

[ведутся работы по улучшению функционала!]
[в дальнейшем текстовые команды будут заменены на кнопки]""")


# команда чата /shorten
async def shorten(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # сообщение пользователю
    if not context.args:
        await update.message.reply_text("Используй: /shorten https://example.com")
        return

    long_url = context.args[0]

    # проверка существования ссылки в БД
    existing_short_code = await get_short_code_by_long_url(long_url)

    if existing_short_code:
        # возврат существующей ссылки
        await update.message.reply_text(
            f"Такая ссылка уже есть: {get_full_short_url(existing_short_code)}"
        )
        return

    # создание короткого кода
    short_code = generate_short_code()
    while await link_exists(short_code):  # на случай коллизии
        short_code = generate_short_code()

    # сохранение в БД
    await save_link(short_code, long_url)

    # возврат новой ссылки
    await update.message.reply_text(
        f"Короткая ссылка: {get_full_short_url(short_code)}"
    )


# обработчик команд из чата
def get_application(token: str) -> Application:
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("shorten", shorten))
    return app