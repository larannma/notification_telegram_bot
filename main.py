import Constants
from Postgres.Connection import DB

from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import asyncio

import os
from datetime import date
from dotenv import load_dotenv

from telegram import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    Update
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

from telegram.constants import ParseMode


db = DB()
load_dotenv()

#define states and bot token
MENU, ASK_NAME, ASK_NOTIFICATION, ASK_DATE, ASK_RATE = range(5)
BOT_TOKEN = os.getenv('BOT_TOKEN')

# start function
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

# Menu function
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


# "Set Notification" function
async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    name = update.message.text
    context.user_data["name"] = name

    await update.message.reply_text("Enter your notification")
    return ASK_NOTIFICATION

async def ask_notification(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    notification = update.message.text
    context.user_data["text"] = notification

    await update.message.reply_text("Enter your date in the type --> yyyy-MM-dd")
    return ASK_DATE

async def ask_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    date_str = update.message.text
    date_obj = date.fromisoformat(date_str)
    context.user_data["date"] = date_obj

    temp = db.checkTGId(str(context.user_data["tg_id"]))

    if temp is not None:
        db.insert_notification(temp, context.user_data["text"], context.user_data["date"])

    else:
        userId = db.insert_user(context.user_data["tg_id"], context.user_data["name"])
        db.insert_notification(userId, context.user_data["text"], context.user_data["date"])

    # return to menu
    keyboard = [
        [InlineKeyboardButton("Set Notification", callback_data="Set Notification")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose the command:", reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    return MENU



# Resend notifications to users
async def sendDueNoifications(application: Application):
    due_massages = db.getDueMessage()
    for msg in due_massages:
        user_id = msg["user_id"]
        text = msg["notifications"]
        await application.bot.send_message(chat_id=user_id, text=text)
        db.markMessageAsSent(msg["id"])

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

# Main function
def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()    

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        lambda: asyncio.run(sendDueNoifications(application)),
        trigger=IntervalTrigger(minutes=1),
        id='send_nitifications',
        replace_existing=True
    )
    scheduler.start()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            # setup "Menu" function
            MENU: [CallbackQueryHandler(menu)],

            # setup "Set Notification" function
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
            ASK_NOTIFICATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_notification)],
            ASK_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_date)],
            #ASK_RATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_rate)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )


    # Start The Bot
    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()
