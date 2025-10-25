import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatMember
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
import yt_dlp

from flask import Flask
from threading import Thread

import database

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

async def is_user_admin(update: Update, context: CallbackContext, user_id: int) -> bool:
    chat = update.effective_chat
    if chat.type == "private":
        return True
    
    try:
        member = await context.bot.get_chat_member(chat.id, user_id)
        return member.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]
    except Exception as e:
        logger.error(f"Error checking admin status: {e}")
        return False

async def prompt_admin_for_deletion_setting(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("Yes, delete after processing", callback_data="delete_yes"),
            InlineKeyboardButton("No, keep files", callback_data="delete_no")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Would you like me to delete the audio files after sending them to you? "
        "This helps save storage space.",
        reply_markup=reply_markup
    )

async def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    await update.message.reply_text(
        'Hi! Send me a YouTube link and I\'ll convert it to MP3 for you! 🎵'
    )
    
    admin_prompted = await database.get_admin_prompted(chat_id)
    if not admin_prompted and await is_user_admin(update, context, user_id):
        await prompt_admin_for_deletion_setting(update, context)
        await database.set_admin_prompted(chat_id, True)

async def download_audio(update: Update, context: CallbackContext):
    """Download YouTube video as MP3."""
    url = update.message.text
    chat_id = update.effective_chat.id
    message_id = update.message.message_id
    
    if await database.is_message_processed(chat_id, message_id):
        logger.debug(f"Message {message_id} already processed, skipping")
        return
    
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
            sent_message = await update.message.reply_audio(audio=audio)
        
        await database.mark_message_processed(chat_id, message_id)
        
        if sent_message.audio:
            await database.mark_audio_processed(sent_message.audio.file_id)
        
        delete_after = await database.get_delete_after_transcription(chat_id)
        if delete_after:
            os.remove(mp3_file)
            logger.info(f"Deleted MP3 file for chat {chat_id} per settings")
        else:
            logger.info(f"Kept MP3 file for chat {chat_id} per settings")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(f'Sorry, an error occurred: {str(e)}')

async def handle_deletion_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    
    chat_id = update.effective_chat.id
    delete_setting = query.data == "delete_yes"
    
    await database.set_delete_after_transcription(chat_id, delete_setting)
    
    if delete_setting:
        message = (
            "✅ Audio files will be deleted after processing to save storage space.\n\n"
            "To change this setting later, send 'change' or mention me with '@bot change' in groups."
        )
    else:
        message = (
            "✅ Audio files will be kept after processing.\n\n"
            "To change this setting later, send 'change' or mention me with '@bot change' in groups."
        )
    
    await query.edit_message_text(text=message)
    logger.info(f"Chat {chat_id}: Deletion setting set to {delete_setting}")

async def handle_change_command(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    if not await is_user_admin(update, context, user_id):
        await update.message.reply_text("Sorry, only administrators can change this setting.")
        return
    
    current_setting = await database.get_delete_after_transcription(chat_id)
    new_setting = not current_setting
    
    await database.set_delete_after_transcription(chat_id, new_setting)
    
    if new_setting:
        message = "✅ Changed: Audio files will now be deleted after processing."
    else:
        message = "✅ Changed: Audio files will now be kept after processing."
    
    await update.message.reply_text(message)
    logger.info(f"Chat {chat_id}: Admin {user_id} toggled deletion setting to {new_setting}")

async def handle_text_message(update: Update, context: CallbackContext):
    text = update.message.text.strip()
    
    bot_username = context.bot.username
    mention_pattern = f"@{bot_username}"
    
    if text.lower() == "change" or (mention_pattern in text and "change" in text.lower()):
        await handle_change_command(update, context)
    elif 'youtube.com' in text or 'youtu.be' in text:
        await download_audio(update, context)
    else:
        await update.message.reply_text('Please send a valid YouTube link!')

async def process_startup_history(application: Application):
    logger.info("Processing startup history for unprocessed messages...")
    
    chat_ids = await database.get_all_chat_ids()
    
    for chat_id in chat_ids:
        try:
            chat = await application.bot.get_chat(chat_id)
            logger.info(f"Checking chat {chat_id} ({chat.title if chat.title else 'DM'}) for unprocessed messages")
        except Exception as e:
            logger.error(f"Error accessing chat {chat_id}: {e}")
    
    logger.info("Startup history processing complete")

async def post_init(application: Application):
    database.init_database()
    logger.info("Database initialized")
    await process_startup_history(application)

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_deletion_callback, pattern="^delete_"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    
    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    keep_alive()
    main()