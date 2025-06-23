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
    # === INVESTERINGANALYSE ===

INVESTMENT_MAP = [
    {
        "keywords": ["iran", "olie", "drone", "houthi", "tankers", "strait of hormuz"],
        "stock": "XOM",
        "reason": "Olie-aanval: ExxonMobil stijgt vaak bij spanningen in Midden-Oosten",
        "gain": 0.05
    },
    {
        "keywords": ["cyberaanval", "hack", "ransomware", "banken", "bank"],
        "stock": "CRWD",
        "reason": "Cyberaanval: CrowdStrike profiteert van verhoogde vraag naar beveiliging",
        "gain": 0.06
    },
    {
        "keywords": ["nato", "navo", "wapenlevering", "militaire steun", "ukraine", "escalatie"],
        "stock": "LMT",
        "reason": "NAVO-escalatie: Lockheed Martin stijgt vaak bij wapenleveringen",
        "gain": 0.08
    },
    {
        "keywords": ["blokkade", "scheepvaart", "haven", "container", "zee", "rode zee"],
        "stock": "Maersk",
        "reason": "Scheepvaart-blokkade: Maersk stijgt bij hogere transportprijzen",
        "gain": 0.04
    },
    {
        "keywords": ["sanctie", "chips", "exportverbod", "embargo", "nvidia"],
        "stock": "NVDA",
        "reason": "Chip-sancties: NVIDIA stijgt vaak door marktdominantie",
        "gain": 0.07
    }
]

last_sent_titles = []

def analyze_article(title, description):
    content = f"{title.lower()} {description.lower()}"
    for entry in INVESTMENT_MAP:
        if any(keyword in content for keyword in entry["keywords"]):
            if entry["gain"] >= 0.03:
                return entry
    return None

def send_investment_alert(article, analysis):
    message = (
        f"🚨 *Nieuwe gebeurtenis gedetecteerd!*\n\n"
        f"*{article['title']}*\n"
        f"🕒 {article['publishedAt']}\n"
        f"🔗 [Lees artikel]({article['url']})\n\n"
        f"💼 Aandeel: *{analysis['stock']}*\n"
        f"📈 Verwachte winst: *{int(analysis['gain']*100)}%*\n"
        f"💬 Reden: {analysis['reason']}\n"
        f"📌 *Advies*: KOOP {analysis['stock']} – Verkoop bij +{int(analysis['gain']*100)}%\n"
    )
    bot.send_message(chat_id="7721050897", text=message, parse_mode='Markdown')

def fetch_news():
    url = "https://newsapi.org/v2/everything?q=attack OR explosion OR military OR war OR oil OR cyberattack&sortBy=publishedAt&language=en&pageSize=10&apiKey=c3ceb5693e814fb393711c27c90abc4f"
    response = requests.get(url)
    articles = response.json().get("articles", [])

    for article in articles:
        title = article.get("title", "")
        description = article.get("description", "")
        if title in last_sent_titles:
            continue
        analysis = analyze_article(title, description)
        if analysis:
            send_investment_alert(article, analysis)
            last_sent_titles.append(title)
            if len(last_sent_titles) > 50:
                last_sent_titles.pop(0)

def start_monitoring():
    while True:
        fetch_news()
        time.sleep(300)  # elke 5 minuten checken
    
    

