import os
import Constants

from dotenv import(
    load_dotenv
)

from saveToJson import (
    write_json
)

from telegram import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    Update
)

from telegram.ext import (
    Application, 
    CallbackQueryHandler, 
    CommandHandler, 
    ContextTypes, 
    MessageHandler, 
    filters
)


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        Constants.GREETINGS
    )

#define states
ASK_NAME, ASK_NOTIFICATION, ASK_DATE, ASK_RATE = range(5)

async def Menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Set Notification", callback_data="Set Notification")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(text=f"Selected option: {query.data}")

# --------

async def set_notification(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text
    context.user_data['name'] = message_text
    print(context.user_data)

def main() -> None:

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, set_notification))

    # Menu buttons
    application.add_handler(CommandHandler("menu", Menu))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()