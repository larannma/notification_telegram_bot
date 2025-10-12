# poject imports
from PostgresDataBase.Connection import DataBase

# lib imports
import os
from telegram import Bot
from dotenv import load_dotenv


load_dotenv()
database_class = DataBase()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)


# "Sent Notification" function
class SendNotification:
    async def send_notification(self, temp):
        print("a")
        messages = database_class.get_messages()
        print("b", messages)
        if len(messages) == 0:
            return

        for i in range(len(messages)):
            user_id = database_class.get_user(messages[i]["user_id"])
            await bot.send_message(
                chat_id=int(user_id[0][0]), text=messages[i]["text"]
            )

            database_class.mark_message_as_sent(messages[i]["id"])
