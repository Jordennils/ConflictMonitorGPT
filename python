import os
from telegram import Bot
import time

def main():
    bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    bot.send_message(chat_id=chat_id, text="⚠️ TEST melding: systeem is live!")
    time.sleep(2)

if __name__ == "__main__":
    main()
