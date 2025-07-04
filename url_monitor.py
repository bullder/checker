import os
import time
import hashlib
import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
URL_TO_MONITOR = os.getenv("URL_TO_MONITOR")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))  # Time in seconds between checks
NOTIFY_ON_NO_CHANGE = os.getenv("NOTIFY_ON_NO_CHANGE", "false").lower() == "true"


def get_website_hash(url):
    """Fetches the content of a URL and returns its SHA-256 hash."""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()  # Raise an exception for bad status codes
        return hashlib.sha256(response.content).hexdigest()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def send_telegram_notification(bot, chat_id, message):
    """Sends a message to a Telegram chat."""
    try:
        bot.send_message(chat_id=chat_id, text=message)
        print("Telegram notification sent.")
    except telegram.error.TelegramError as e:
        print(f"Error sending Telegram notification: {e}")

def main():
    """Main function to monitor the website."""
    if not all([URL_TO_MONITOR, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]):
        print("Please set the environment variables URL_TO_MONITOR, TELEGRAM_BOT_TOKEN, and TELEGRAM_CHAT_ID.")
        return

    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    last_hash = get_website_hash(URL_TO_MONITOR)

    if last_hash:
        print(f"Started monitoring {URL_TO_MONITOR}")
        print(f"Initial hash: {last_hash}")

    while True:
        time.sleep(CHECK_INTERVAL)
        current_hash = get_website_hash(URL_TO_MONITOR)

        if current_hash and current_hash != last_hash:
            print(f"Change detected at {URL_TO_MONITOR}")
            print(f"New hash: {current_hash}")
            send_telegram_notification(
                bot,
                TELEGRAM_CHAT_ID,
                f"Change detected on {URL_TO_MONITOR}! A new version of the page is available.",
            )
            last_hash = current_hash
        elif not current_hash:
            print("Could not fetch website content. Will try again later.")
        elif NOTIFY_ON_NO_CHANGE:
            print(f"No change detected at {URL_TO_MONITOR}. Sending health check notification.")
            send_telegram_notification(
                bot,
                TELEGRAM_CHAT_ID,
                f"Health check: No change detected on {URL_TO_MONITOR}.",
            )

if __name__ == "__main__":
    main()
