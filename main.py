import os
import Constants

from dotenv import(
    load_dotenv
)

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

from telegram.constants import (
    ParseMode
)

load_dotenv()

#define states and bot token
MENU, ASK_NAME, ASK_NOTIFICATION, ASK_DATE, ASK_RATE = range(5)
BOT_TOKEN = os.getenv('BOT_TOKEN')


# start function
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    userId = update.effective_user.id
    context.user_data["userId"] = userId

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
    context.user_data["notification"] = notification

    await update.message.reply_text("Enter your date for sending your notification")
    return ASK_DATE

async def ask_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    date = update.message.text
    context.user_data["date"] = date

    await update.message.reply_text("Enter your rate of sending your notification")
    return ASK_RATE

async def ask_rate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    rate = update.message.text
    context.user_data["rate"] = rate
    print(context.user_data)

    return ConversationHandler.END

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
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
            ASK_NOTIFICATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_notification)],
            ASK_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_date)],
            ASK_RATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_rate)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Start The Bot
    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()