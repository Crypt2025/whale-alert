import feedparser
import requests
import os

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
RSS_FEED_URL = 'https://nitter.net/whale_alert/rss'
MIN_BTC = 100

def parse_rss():
    feed = feedparser.parse(RSS_FEED_URL)
    alerts = []
    for entry in feed.entries:
        title = entry.title
        if 'BTC' in title:
            try:
                amount_str = title.split(' BTC')[0].split()[-1].replace(',', '')
                btc_amount = float(amount_str)
                if btc_amount >= MIN_BTC:
                    alerts.append(f"{title}\n{entry.link}")
            except Exception:
                continue
    return alerts

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': msg}
    response = requests.post(url, data=payload)
    print(f"Telegram API Response: {response.status_code} - {response.text}")

if __name__ == "__main__":
    alerts = parse_rss()
    if not alerts:
        send_telegram("✅ Testlauf erfolgreich: Keine Whale-Transaktion gefunden, aber der Bot funktioniert!")
    else:
        for alert in alerts:
            send_telegram(f"🐋 Neue BTC-Transaktion entdeckt:\n{alert}")
