"""Entry point for the package: python -m meet_bot
"""
import os
import logging
from dotenv import load_dotenv

from .bot import create_bot, register_handlers
from .web import create_app, run

logging.basicConfig(level=logging.INFO)

def main():
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    mode = os.getenv("MODE", "polling").lower()
    
    bot = create_bot(token)
    register_handlers(bot)
    
    if mode == "webhook":
        # Webhook mode (for production/deployed environments)
        app = create_app(bot, token=token)
        # Azure App Service uses WEBSITES_PORT, fallback to PORT, then 8000
        port = int(os.getenv("WEBSITES_PORT", os.getenv("PORT", "8000")))
        run(app, host="0.0.0.0", port=port)
    else:
        # Polling mode (for local testing)
        logging.info("Starting bot in polling mode...")
        logging.info("Bot is ready! Send /start or /meet commands in Telegram")
        bot.infinity_polling()

if __name__ == "__main__":
    main()
