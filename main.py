import os
import time
import requests
from telegram import Bot
from datetime import datetime, timedelta

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
chat_id = os.getenv("TELEGRAM_CHAT_ID")
NEWSAPI_KEY = "c3ceb5693e814fb393711c27c90abc4f"

KEYWORDS = [
    "drone attack oil", "missile strike", "port blockade", "cyberattack bank",
    "NATO weapons delivery", "unannounced sanctions", "chip embargo", "military escalation"
]

last_sent_titles = []

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

def check_newsapi():
    url = f"https://newsapi.org/v2/everything?q={' OR '.join(KEYWORDS)}&language=en&sortBy=publishedAt&pageSize=10&apiKey={NEWSAPI_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    print(f"[DEBUG] 🔍 Aantal artikelen opgehaald: {len(articles)}")
    relevant = []

    for article in articles:
        title = article.get("title", "")
        published_at = article.get("publishedAt", "")
        if title and title not in last_sent_titles:
            published_time = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
            if datetime.utcnow() - published_time < timedelta(minutes=10):
                print(f"[DEBUG] ✅ Relevante titel gevonden (binnen 10 minuten): {title}")
                last_sent_titles.append(title)
                if len(last_sent_titles) > 100:
                    last_sent_titles.pop(0)
                relevant.append(article)
            else:
                print(f"[DEBUG] ⏰ Ouder dan 10 minuten: {title}")
        else:
            print(f"[DEBUG] ❌ Dubbele of lege titel: {title}")

    return relevant

def analyze_article(title, description):
    content = f"{title.lower()} {description.lower()}"
    for entry in INVESTMENT_MAP:
        if any(keyword.lower() in content for keyword in entry["keywords"]):
            if entry["gain"] >= 0.03:
                print(f"[DEBUG] 📈 Investeringsmatch gevonden: {entry['stock']}")
                return entry
    print(f"[DEBUG] ❌ Geen investeringsmatch voor: {title}")
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
    bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

def start_monitoring():
    while True:
        try:
            articles = check_newsapi()
            for article in articles:
                title = article.get("title", "")
                description = article.get("description", "")
                analysis = analyze_article(title, description)
                if analysis:
                    send_investment_alert(article, analysis)
        except Exception as e:
            print(f"[FOUT] 🛑 Tijdens monitoring: {e}")

        time.sleep(300)  # 5 minuten

if __name__ == "__main__":
    start_monitoring()
