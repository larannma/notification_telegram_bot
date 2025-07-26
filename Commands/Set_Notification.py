# poject imports
from PostgresDataBase.Connection import DataBase
from Helper.Date_Formating import DateFormating

# lib imports
import datetime

from telegram import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    Update
)
from telegram.ext import (
    ContextTypes, 
)

from telegram.constants import ParseMode

MENU_HANDLER, ASK_NAME, ASK_NOTIFICATION, DATE_BUTTON_HANDLER, SET_MY_DATE, ASK_TIME = range(6)
database_class = DataBase()
date_formating_class = DateFormating()


# "Set Notification" function
class SetNotification():
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
            [InlineKeyboardButton("Sent after day", callback_data="Sent after day")],
            [InlineKeyboardButton("Sent after week", callback_data="Sent after week")],
            [InlineKeyboardButton("Choose my date", callback_data="Choose my date")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("Please choose the variation:",reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        return DATE_BUTTON_HANDLER


    
    async def date_button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=f"Selected option: {query.data}")

        # Sent after day function
        if query.data == "Sent after day":
            context.user_data["date"] = date_formating_class.date_formting(1)
            
            temp = database_class.check_tg_id(str(context.user_data["tg_id"]))
            if temp is not None:
                database_class.insert_notification(
                    temp,
                    context.user_data["text"],
                    context.user_data["date"]
                )
                
            else:
                userId = database_class.insert_user(context.user_data["tg_id"], context.user_data["name"])
                database_class.insert_notification(
                    userId,
                    context.user_data["text"],
                    context.user_data["date"]
                )
            
            # return to menu
            keyboard = [
                [InlineKeyboardButton("Set Notification", callback_data="Set Notification")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.message.reply_text("Please choose the command:", reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
            return MENU_HANDLER

        
        
        
        
        
        # Sent after week function
        if query.data == "Sent after week":
            context.user_data["date"] = date_formating_class.date_formting(7)
            
            temp = database_class.check_tg_id(str(context.user_data["tg_id"]))
            if temp is not None:
                database_class.insert_notification(
                    temp,
                    context.user_data["text"],
                    context.user_data["date"]
                )
                
            else:
                userId = database_class.insert_user(context.user_data["tg_id"], context.user_data["name"])
                database_class.insert_notification(
                    userId,
                    context.user_data["text"],
                    context.user_data["date"]
                )
            
            # return to menu
            keyboard = [
                [InlineKeyboardButton("Set Notification", callback_data="Set Notification")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.message.reply_text("Please choose the command:", reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
            return MENU_HANDLER






        # Choose my date function
        if query.data == "Choose my date":
            await query.message.reply_text("Enter date when to sent your notification: dd MM yyyy")
            return SET_MY_DATE
        
        else:
            keyboard = [
                [InlineKeyboardButton("Set Notification", callback_data="Set Notification")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.message.reply_text("Please choose the command:", reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
            return MENU_HANDLER


    
    async def set_my_date(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        DateStr = update.message.text
        dateList = DateStr.split(" ")
        FinalDate = datetime.datetime(int(dateList[2]), int(dateList[1]), int(dateList[0]), int(dateList[3]), int(dateList[4]), 0)

       
        formatted_date = datetime.datetime.fromtimestamp(FinalDate.timestamp()).strftime('%Y-%m-%d %H:%M:%S')
        context.user_data["date"] = formatted_date
        temp = database_class.check_tg_id(str(context.user_data["tg_id"]))

        if temp is not None:
            database_class.insert_notification(
                temp,
                context.user_data["text"],
                context.user_data["date"]
            )
            
        else:
            userId = database_class.insert_user(context.user_data["tg_id"], context.user_data["name"])
            database_class.insert_notification(
                userId,
                context.user_data["text"],
                context.user_data["date"]
            )
        
        # return to menu
        keyboard = [
            [InlineKeyboardButton("Set Notification", callback_data="Set Notification")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("Please choose the command:", reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        return MENU_HANDLER
