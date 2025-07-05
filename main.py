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

async def check_status():
    a = db.getMessages()
    print(a is not None)

async def sent_notification():
    a = db.getMessages()
    print(a, len(a))
    if len(a) == 0:
        return
    
    for i in range(len(a)):
        b = db.getUser(a[i]['user_id'])
        await bot.send_message(chat_id=int(b[0][0]), text=a[i]['text'])

        db.markMessageAsSent(a[i]['id'])

        print(b[0][0])


def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        lambda: asyncio.run_coroutine_threadsafe(sent_notification(), loop),
        'interval',
        seconds=5
    )
    scheduler.start()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MENU: [CallbackQueryHandler(menu)],
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, SN.ask_name)],
            ASK_NOTIFICATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, SN.ask_notification)],
            ASK_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, SN.ask_date)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_message=True
    )

    application.add_handler(conv_handler)
    application.run_polling()



if __name__ == "__main__":
    main()
