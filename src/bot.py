from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from database import save_link, link_exists, get_short_code_by_long_url
from utils import generate_short_code, is_valid_url
from config import get_full_short_url


# создает инлайн-кнопки с действиями
def get_main_keyboard():
    button_shorten = InlineKeyboardButton(text="🔗 Укоротить ссылку", callback_data="shorten")
    button_info = InlineKeyboardButton(text="ℹ️ О боте", callback_data="info")
    button_close = InlineKeyboardButton(text="❌ Закрыть меню", callback_data="close")
    keyboard = [
        [button_shorten],
        [button_info, button_close]
    ]
    return InlineKeyboardMarkup(keyboard)


# обработчик нажатия на кнопки
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "shorten":
        await query.edit_message_text(
            "🔗 Скинь длинную ссылку, а я укорочу ее.\n"
            "Например: https://example.com 🦐"
        )
        context.user_data['waiting_for_link'] = True
    elif data == "info":
        await query.edit_message_text(
            "⛓️ Бот укревечивает ссылки 🦐\n"
            "Жми на кнопку и отправляй мне ссылку.",
        reply_markup=get_main_keyboard()
        )
    elif data == "close":
        await query.edit_message_text("Меню закрыто. Тыкай /start, чтобы открыть снова.")
    else:
        await query.edit_message_text("💀 Неизвестная команда.")


# обработчик текстовых сообщений (ссылка)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('waiting_for_link'):
        long_url = update.message.text

        if not is_valid_url(long_url):
            await update.message.reply_text(
                "❌ Это не похоже на ссылку.\n"
                "Проверь, что ссылка начинается с http:// или https://\n"
                "и что после них есть домен (например: https://example.com)"
            )
            return

        existing_short_code = await get_short_code_by_long_url(long_url)
        if existing_short_code:
            short_url = get_full_short_url(existing_short_code)
            await update.message.reply_text(f"Такая ссылка уже есть: {short_url}",
        reply_markup=get_main_keyboard())
        else:
            short_code = generate_short_code()
            while await link_exists(short_code):
                short_code = generate_short_code()
            await save_link(short_code, long_url)
            short_url = get_full_short_url(short_code)
            await update.message.reply_text(f"Короткая ссылка: {short_url}",
        reply_markup=get_main_keyboard())

        context.user_data['waiting_for_link'] = False
    else:
        await update.message.reply_text("Нажми /start, чтобы открыть меню.")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = get_main_keyboard()
    await update.message.reply_text(
        "Бот работает! \n[ведутся работы по улучшению функционала!] \n\nВыбери действие:",
        reply_markup=reply_markup
    )


def get_application(token: str) -> Application:
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return app