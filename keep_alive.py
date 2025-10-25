from flask import Flask
from threading import Thread
import config

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/health')
def health():
    return {"status": "healthy", "message": "Telegram bot is alive"}

def run():
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT)

def keep_alive():
    """Start the Flask server in a separate thread to keep the bot alive on Replit."""
    t = Thread(target=run)
    t.daemon = True
    t.start()
