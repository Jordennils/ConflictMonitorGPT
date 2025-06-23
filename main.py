import os
import time
import requests
from telegram import Bot
from datetime import datetime, timedelta

# Telegram instellingen
bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
chat_id = os.getenv("TELEGRAM_CHAT_ID")

# NewsAPI sleutel
NEWSAPI_KEY = "c3ceb5693e814fb393711c27c90abc4f"

# Wat we zoeken (conflict triggers)
KEYWORDS = [
    "drone attack oil", "missile strike", "port blockade", "cyberattack bank",
    "NATO weapons delivery", "unannounced sanctions", "chip embargo", "military escalation"
]

# Timestamp om dubbele meldingen te vermijden
last_sent_titles = set()

def check_newsapi():
    url = f"https://newsapi.org/v2/everything?q={' OR '.join(KEYWORDS)}&language=en&sortBy=publishedAt&pageSize=5&apiKey={NEWSAPI_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    relevant = []

    for article in articles:
        title = article["title"]
        if title not in last_sent_titles:
            last_sent_titles.add(title)
            relevant.append(article)

    return relevant

def send_telegram_alert(article):
    title = article.get("title", "Geen titel")
    url = article.get("url", "Geen link")
    time_published = article.get("publishedAt", "Onbekend")
    message = f"🚨 *Nieuwe gebeurtenis gedetecteerd!*\n\n*{title}*\n🕒 {time_published}\n🔗 [Lees artikel]({url})"
    bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")

def monitor():
    while True:
        try:
            articles = check_newsapi()
            for article in articles:
                send_telegram_alert(article)
        except Exception as e:
            print(f"Fout tijdens controleren of verzenden: {e}")

        time.sleep(300)  # elke 5 minuten

if __name__ == "__main__":
    monitor()
