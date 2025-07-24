import feedparser
import requests
import os

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
RSS_FEED_URL = 'https://rsshub.app/telegram/channel/WhaleBotAlerts'
MIN_BTC = 10  # Minimum BTC-Menge (z. B. 1 oder 10)

def parse_rss():
    feed = feedparser.parse(RSS_FEED_URL)
    alerts = []
    for entry in feed.entries:
        title = entry.title
        if 'BTC' in title and 'Exchange' not in title:
            try:
                amount_str = title.split('BTC')[0].split()[-1].replace(',', '')
                btc_amount = float(amount_str)
                if btc_amount >= MIN_BTC:
                    alerts.append(f"{title}\n{entry.link}")
            except Exception as e:
                print(f"Fehler beim Parsen: {e}")
    return alerts

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': msg}
    requests.post(url, data=payload)

if __name__ == "__main__":
    alerts = parse_rss()
    if not alerts:
        send_telegram("🔍 Kein neuer BTC-Transfer gefunden.")
    for alert in alerts:
        send_telegram(f"🐋 Neue BTC-Transaktion:\n{alert}")
