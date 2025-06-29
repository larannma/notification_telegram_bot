# poject imports
import Helper.Constants as Constants
from Commands.SetNotification import Set_Notification
from Postgres.Connection import DB

# lib imports
import os, asyncio
from dotenv import load_dotenv
from datetime import datetime, date, time
from apscheduler.schedulers.background import BackgroundScheduler

from telegram.constants import ParseMode
from telegram import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    Update,
    Bot
)
from telegram.ext import (
    Application, 
    CallbackQueryHandler,
    ConversationHandler,
    CommandHandler, 
    ContextTypes, 
    MessageHandler, 
    filters
)


load_dotenv()
SN = Set_Notification()
db = DB()

# define states
MENU, ASK_NAME, ASK_NOTIFICATION, ASK_DATE, ASK_RATE = range(5)
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    tg_id = update.effective_user.id
    context.user_data["tg_id"] = tg_id

    await update.message.reply_html(
        Constants.GREETINGS
    )

    keyboard = [
        [InlineKeyboardButton("Set Notification", callback_data="Set Notification")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose the command:", reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    return MENU


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"Selected option: {query.data}")

    if query.data == "Set Notification":
        await query.message.reply_text("Enter your name")
        return ASK_NAME
    
    else:
        keyboard = [
            [InlineKeyboardButton("Set Notification", callback_data="Set Notification")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text("Please choose the command:", reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        return MENU



# clean for fallbacks
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END


async def privet():
    a = db.getMessages()
    b = db.getUser(a[0]['user_id'])
    print("rr")
    await bot.send_message(chat_id=993700847, text="kek")

    print(b[0][0])


def wrapper():
    loop = asyncio.get_event_loop()
    loop.create_task(privet())

# Main function
def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()


    scheduler = BackgroundScheduler()
    scheduler.add_job(
        wrapper,
        'interval',
        seconds=5
    )
    scheduler.start()


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            # setup "Menu" function
            MENU: [CallbackQueryHandler(menu)],

            # setup "Set Notification" function
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, SN.ask_name)],
            ASK_NOTIFICATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, SN.ask_notification)],
            ASK_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, SN.ask_date)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )


    # Start The Bot
    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()
