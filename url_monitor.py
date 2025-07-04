import asyncio
import os
import time
import hashlib
import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
URL_TO_MONITOR: str | None = os.getenv("URL_TO_MONITOR")
TELEGRAM_BOT_TOKEN: str | None = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID: str | None = os.getenv("TELEGRAM_CHAT_ID")
CHECK_INTERVAL: int = int(os.getenv("CHECK_INTERVAL", 60))  # Time in seconds between checks
NOTIFY_ON_NO_CHANGE: bool = os.getenv("NOTIFY_ON_NO_CHANGE", "false").lower() == "true"


def get_website_hash(url: str) -> str | None:
    """Fetches the content of a URL and returns its SHA-256 hash."""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()  # Raise an exception for bad status codes
        return hashlib.sha256(response.content).hexdigest()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

async def send_telegram_notification(bot: telegram.Bot, chat_id: str, message: str) -> None:
    """Sends a message to a Telegram chat."""
    try:
        await bot.send_message(chat_id=chat_id, text=message)
        print("Telegram notification sent.")
    except telegram.error.TelegramError as e:
        print(f"Error sending Telegram notification: {e}")

async def main() -> None:
    """Main function to monitor the website."""
    if not all([URL_TO_MONITOR, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]):
        print("Please set the environment variables URL_TO_MONITOR, TELEGRAM_BOT_TOKEN, and TELEGRAM_CHAT_ID.")
        return

    assert URL_TO_MONITOR is not None
    assert TELEGRAM_BOT_TOKEN is not None
    assert TELEGRAM_CHAT_ID is not None

    url_to_monitor: str = URL_TO_MONITOR
    telegram_bot_token: str = TELEGRAM_BOT_TOKEN
    telegram_chat_id: str = TELEGRAM_CHAT_ID

    bot = telegram.Bot(token=telegram_bot_token)
    last_hash = get_website_hash(url_to_monitor)

    if last_hash:
        print(f"Started monitoring {url_to_monitor}")
        print(f"Initial hash: {last_hash}")

    while True:
        time.sleep(CHECK_INTERVAL)
        current_hash = get_website_hash(url_to_monitor)

        if current_hash and current_hash != last_hash:
            print(f"Change detected at {url_to_monitor}")
            print(f"New hash: {current_hash}")
            await send_telegram_notification(
                bot,
                telegram_chat_id,
                f"Change detected on {url_to_monitor}! A new version of the page is available.",
            )
            last_hash = current_hash
        elif not current_hash:
            print("Could not fetch website content. Will try again later.")
        elif NOTIFY_ON_NO_CHANGE:
            print(f"No change detected at {url_to_monitor}. Sending health check notification.")
            await send_telegram_notification(
                bot,
                telegram_chat_id,
                f"Health check: No change detected on {url_to_monitor}.",
            )

if __name__ == "__main__":
    asyncio.run(main())
