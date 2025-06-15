# poject imports
import Helper.Constants as Constants
from Commands.SetNotification import Set_Notification

# lib imports
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
load_dotenv()

SN = Set_Notification()

# define states
MENU, ASK_NAME, ASK_NOTIFICATION, ASK_DATE, ASK_RATE = range(5)
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






# Main function
def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()    


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
