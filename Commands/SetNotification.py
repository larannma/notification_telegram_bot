# lib imports
import datetime
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

MENU_HANDLER, ASK_NAME, ASK_NOTIFICATION, DATE_HANDLER, SENT_AFTER_DAY, SET_MY_DATE, ASK_TIME = range(7)
db = DB()

# "Set Notification" function
class Set_Notification():
    async def ask_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        name = update.message.text
        context.user_data["name"] = name

        await update.message.reply_text("Enter your notification")
        return ASK_NOTIFICATION



    async def ask_notification(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        notification = update.message.text
        context.user_data["text"] = notification

        await update.message.reply_text("Choose the date when to sent your notification")
        keyboard = [
            [InlineKeyboardButton("After day", callback_data="D")],
            [InlineKeyboardButton("After week", callback_data="W")],
            [InlineKeyboardButton("Choose my date", callback_data="MD")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("Please choose the variation:",reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        return DATE_HANDLER





    async def date_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=f"Selected option: {query.data}")

        tg_id = db.checkTGId(str(context.user_data["tg_id"]))

        if query.data == "D":
            await query.message.reply_text("Your message will sent you tomorow")
            return SENT_AFTER_DAY
        
        elif query.data == "W":
            pass

        elif query.data == "MD":
            await query.message.reply_text("Enter your date: dd MM YYYY")
            return SET_MY_DATE

        else:
            keyboard = [
                [InlineKeyboardButton("Set Notification", callback_data="Set Notification")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.message.reply_text("Please choose the command:", reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
            return MENU_HANDLER




    
    async def sent_after_day(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        tg_id = db.checkTGId(str(context.user_data["tg_id"]))

        dateNow = datetime.datetime.now()
        DayPOne = dateNow.day + 1
        FinalDate = datetime.date(dateNow.year, dateNow.month, DayPOne)


        db.insert_notification(tg_id, context.user_data["text"], FinalDate)
        return ASK_TIME
    





    async def set_my_date(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        tg_id = db.checkTGId(str(context.user_data["tg_id"]))

        DateStr = update.message.text
        dateList = DateStr.split(" ")
        FinalDate = datetime.date(int(dateList[2]), int(dateList[1]), int(dateList[0]))

        db.insert_notification(tg_id, context.user_data["text"], FinalDate)
        return ASK_TIME



    async def ask_time(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("кек")
        # return to menu
        keyboard = [
            [InlineKeyboardButton("Set Notification", callback_data="Set Notification")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("Please choose the command:", reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        return MENU_HANDLER
