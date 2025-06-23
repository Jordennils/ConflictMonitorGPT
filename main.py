import os
from telegram import Bot

# Haal token en chat-ID uit omgevingsvariabelen
bot = Bot(token=os.environ.get("TELEGRAM_BOT_TOKEN"))
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

def send_test_message():
    bot.send_message(chat_id=chat_id, text="✅ TEST: Melding ontvangen! Bot werkt correct.")

if __name__ == "__main__":
    send_test_message()
