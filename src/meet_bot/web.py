from flask import Flask, request, abort
import os
import logging
import telebot
from typing import Optional

logging.basicConfig(level=logging.INFO)


def create_app(bot: telebot.TeleBot, token: Optional[str] = None) -> Flask:
    token = token or os.getenv("BOT_TOKEN")
    app = Flask(__name__)

    @app.route("/webhook", methods=["POST"])
    def webhook():
        try:
            if request.headers.get('content-type') == 'application/json':
                json_string = request.get_data().decode('utf-8')
                logging.info(f"Received update: {json_string[:200]}")
                update = telebot.types.Update.de_json(json_string)
                bot.process_new_updates([update])
                return ''
            else:
                abort(403)
        except Exception as e:
            logging.exception(f"Error processing webhook: {e}")
            return '', 500

    @app.route("/")
    def health():
        return "Bot alive!"

    return app

def run(app: Flask, host: str = "0.0.0.0", port: int = 8000):
    app.run(host=host, port=port)
