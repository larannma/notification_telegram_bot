# poject imports
import Helper.Constants as Constants
from Commands.Set_Notification import SetNotification
from Commands.Sent_Notification import SentNotification

# lib imports
import os
from dotenv import load_dotenv

from telegram.constants import ParseMode
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


load_dotenv()
set_notification_class = SetNotification()
sent_notification_class = SentNotification()

# define states
MENU_HANDLER, ASK_NAME, ASK_NOTIFICATION, DATE_BUTTON_HANDLER, SET_MY_DATE, ASK_TIME = range(6)
BOT_TOKEN = os.getenv('BOT_TOKEN')


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
    return MENU_HANDLER



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
        return MENU_HANDLER



# clean for fallbacks
async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Operation ended.")
    return ConversationHandler.END



# Main function
def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            # "Menu" as Query Handler
            MENU_HANDLER: [CallbackQueryHandler(menu)],

            # "Set Notification" functions
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_notification_class.ask_name)],
            ASK_NOTIFICATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_notification_class.ask_notification)],

            DATE_BUTTON_HANDLER: [CallbackQueryHandler(set_notification_class.date_button_handler)],

            SET_MY_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_notification_class.set_my_date)],
            ASK_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_notification_class.ask_time)]
        },
        fallbacks=[CommandHandler("end", end)],
    )

    # Start The Bot
    application.add_handler(conv_handler)
    application.job_queue.run_repeating(sent_notification_class.sent_notification, interval=5, first=5)
    application.run_polling()



if __name__ == "__main__":
    main()
