# poject imports
import Helper.Constants as Constants
from Commands.SetNotification import Set_Notification
from Postgres.Connection import DB

# lib imports
import os
from dotenv import load_dotenv
import datetime

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
MENU_HANDLER, ASK_NAME, ASK_NOTIFICATION, DATE_HANDLER, SENT_AFTER_DAY, SET_MY_DATE, ASK_TIME = range(7)
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
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END



async def sent_notification(ff):
    a = db.getMessages()
    if len(a) == 0:
        return
    
    for i in range(len(a)):
        b = db.getUser(a[i]['user_id'])
        await bot.send_message(chat_id=int(b[0][0]), text=a[i]['text'])

        db.markMessageAsSent(a[i]['id'])



# Main function
def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            # "Menu" as Query Handler
            MENU_HANDLER: [CallbackQueryHandler(menu)],

            # "Set Notification" function
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, SN.ask_name)],
            ASK_NOTIFICATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, SN.ask_notification)],

            DATE_HANDLER: [
                CallbackQueryHandler(SN.sent_after_day)
            ],
            SENT_AFTER_DAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, SN.sent_after_day)],
            
            ASK_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, SN.ask_time)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
            # 
            # SET_MY_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, SN.set_my_date)],

    # Start The Bot
    application.add_handler(conv_handler)
    application.job_queue.run_repeating(sent_notification, interval=5, first=5)
    application.run_polling()

if __name__ == "__main__":
    main()
