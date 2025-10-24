import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import yt_dlp

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Get bot token from secrets
BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables!")

async def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        'Hi! Send me a YouTube link and I\'ll convert it to MP3 for you! 🎵'
    )

async def download_audio(update: Update, context: CallbackContext):
    """Download YouTube video as MP3."""
    url = update.message.text
    
    # Check if it's a YouTube URL
    if 'youtube.com' not in url and 'youtu.be' not in url:
        await update.message.reply_text('Please send a valid YouTube link!')
        return
    
    await update.message.reply_text('Downloading... ⏳')
    
    try:
        # Configure yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': True,
        }
        
        # Download the audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            mp3_file = filename.rsplit('.', 1)[0] + '.mp3'
        
        # Send the MP3 file
        await update.message.reply_text('Uploading your MP3... 📤')
        with open(mp3_file, 'rb') as audio:
            await update.message.reply_audio(audio=audio)
        
        # Delete the file to save space
        os.remove(mp3_file)
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(f'Sorry, an error occurred: {str(e)}')

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_audio))
    
    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    keep_alive()
    main()