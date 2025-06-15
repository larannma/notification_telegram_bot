# lib imports
from datetime import date
from Postgres.Connection import DB

from telegram import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    Update
)
from telegram.ext import (
    ContextTypes, 
)

from telegram.constants import ParseMode

MENU, ASK_NAME, ASK_NOTIFICATION, ASK_DATE, ASK_RATE = range(5)
db = DB()

# "Set Notification" function
class Set_Notification():
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
