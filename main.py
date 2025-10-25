import os
import logging
import json
import tempfile
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Set

from telegram import Update, File
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram.error import TelegramError

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

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables!")

ADMIN_USER_IDS = [int(uid.strip()) for uid in os.environ.get('ADMIN_USER_IDS', '').split(',') if uid.strip()]
TRANSCRIPTION_API_KEY = os.environ.get('TRANSCRIPTION_API_KEY', '')
CONFIG_FILE = 'bot_config.json'
MAX_FILE_SIZE_MB = 20
PROCESSED_IDS_LIMIT = 1000

class BotStorage:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.data = self._load()
    
    def _load(self) -> Dict[str, Any]:
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading config: {e}")
        return {
            'processed_message_ids': [],
            'chat_settings': {},
            'pending_configs': {}
        }
    
    def save(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def is_processed(self, message_id: int) -> bool:
        return message_id in self.data['processed_message_ids']
    
    def mark_processed(self, message_id: int):
        if message_id not in self.data['processed_message_ids']:
            self.data['processed_message_ids'].append(message_id)
            if len(self.data['processed_message_ids']) > PROCESSED_IDS_LIMIT:
                self.data['processed_message_ids'] = self.data['processed_message_ids'][-PROCESSED_IDS_LIMIT:]
            self.save()
    
    def get_chat_setting(self, chat_id: int, key: str, default: Any = None) -> Any:
        chat_id_str = str(chat_id)
        return self.data['chat_settings'].get(chat_id_str, {}).get(key, default)
    
    def set_chat_setting(self, chat_id: int, key: str, value: Any):
        chat_id_str = str(chat_id)
        if chat_id_str not in self.data['chat_settings']:
            self.data['chat_settings'][chat_id_str] = {}
        self.data['chat_settings'][chat_id_str][key] = value
        self.save()
    
    def get_pending_config(self, user_id: int) -> Optional[str]:
        return self.data['pending_configs'].get(str(user_id))
    
    def set_pending_config(self, user_id: int, config_type: str):
        self.data['pending_configs'][str(user_id)] = config_type
        self.save()
    
    def clear_pending_config(self, user_id: int):
        user_id_str = str(user_id)
        if user_id_str in self.data['pending_configs']:
            del self.data['pending_configs'][user_id_str]
            self.save()

storage = BotStorage(CONFIG_FILE)

async def transcribe_audio(file_path: str) -> str:
    """
    Transcribe audio file using transcription service.
    This is a placeholder implementation that can be replaced with actual API calls.
    """
    try:
        await asyncio.sleep(0.5)
        
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        
        if TRANSCRIPTION_API_KEY:
            logger.info(f"Transcription API available - would transcribe {file_name}")
        
        return f"[Transcription completed for {file_name} ({file_size} bytes)]\n\nThis is a placeholder transcription. To enable real transcription, configure TRANSCRIPTION_API_KEY environment variable and integrate with your preferred transcription service (e.g., OpenAI Whisper, Google Speech-to-Text, etc.)."
    
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        raise

async def start(update: Update, context: CallbackContext):
    """Handle /start command."""
    user = update.effective_user
    chat_type = update.effective_chat.type
    
    welcome_message = (
        f"👋 Hello {user.first_name}!\n\n"
        "I'm an audio transcription bot. Send me:\n"
        "• Voice messages 🎤\n"
        "• Audio files 🎵\n"
        "• Video notes 🎥\n\n"
        "And I'll transcribe them for you!\n\n"
    )
    
    if user.id in ADMIN_USER_IDS:
        welcome_message += (
            "🔧 Admin commands:\n"
            "/delete_on - Delete audio after transcription (default)\n"
            "/delete_off - Keep audio after transcription\n"
            "/status - View current settings\n"
        )
    
    await update.message.reply_text(welcome_message)

async def status_command(update: Update, context: CallbackContext):
    """Handle /status command."""
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    if user.id not in ADMIN_USER_IDS:
        await update.message.reply_text("⛔ This command is only available to admins.")
        return
    
    delete_after = storage.get_chat_setting(chat_id, 'delete_after_transcription', True)
    
    status_msg = (
        "📊 Current Settings:\n\n"
        f"Chat ID: {chat_id}\n"
        f"Delete after transcription: {'✅ Enabled' if delete_after else '❌ Disabled'}\n"
        f"Admin: {'✅ Yes' if user.id in ADMIN_USER_IDS else '❌ No'}\n"
    )
    
    await update.message.reply_text(status_msg)

async def delete_on_command(update: Update, context: CallbackContext):
    """Enable deleting audio after transcription."""
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    if user.id not in ADMIN_USER_IDS:
        await update.message.reply_text("⛔ This command is only available to admins.")
        return
    
    storage.set_chat_setting(chat_id, 'delete_after_transcription', True)
    await update.message.reply_text("✅ Audio will be deleted after transcription.")

async def delete_off_command(update: Update, context: CallbackContext):
    """Disable deleting audio after transcription."""
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    if user.id not in ADMIN_USER_IDS:
        await update.message.reply_text("⛔ This command is only available to admins.")
        return
    
    storage.set_chat_setting(chat_id, 'delete_after_transcription', False)
    await update.message.reply_text("✅ Audio will be kept after transcription.")

async def handle_audio_message(update: Update, context: CallbackContext):
    """Handle audio, voice, and video note messages."""
    message = update.message
    user = update.effective_user
    chat_id = update.effective_chat.id
    message_id = message.message_id
    
    if storage.is_processed(message_id):
        logger.info(f"Message {message_id} already processed, skipping")
        return
    
    file_obj: Optional[File] = None
    file_type = "audio"
    
    if message.voice:
        file_obj = message.voice
        file_type = "voice"
    elif message.audio:
        file_obj = message.audio
        file_type = "audio"
    elif message.video_note:
        file_obj = message.video_note
        file_type = "video_note"
    else:
        return
    
    file_size_mb = file_obj.file_size / (1024 * 1024) if file_obj.file_size else 0
    
    if file_size_mb > MAX_FILE_SIZE_MB:
        await message.reply_text(
            f"⚠️ File too large ({file_size_mb:.1f}MB). Maximum size is {MAX_FILE_SIZE_MB}MB."
        )
        return
    
    status_message = await message.reply_text("⏳ Processing your audio...")
    
    temp_dir = None
    temp_file_path = None
    
    try:
        temp_dir = tempfile.mkdtemp(prefix='bot_audio_')
        
        file_extension = 'ogg'
        if file_type == 'audio' and hasattr(file_obj, 'mime_type'):
            mime_type = file_obj.mime_type or ''
            if 'mpeg' in mime_type or 'mp3' in mime_type:
                file_extension = 'mp3'
            elif 'mp4' in mime_type or 'm4a' in mime_type:
                file_extension = 'm4a'
            elif 'wav' in mime_type:
                file_extension = 'wav'
        
        temp_file_path = os.path.join(temp_dir, f"audio_{message_id}.{file_extension}")
        
        telegram_file = await context.bot.get_file(file_obj.file_id)
        await telegram_file.download_to_drive(temp_file_path)
        
        logger.info(f"Downloaded {file_type} from user {user.id} to {temp_file_path}")
        
        await status_message.edit_text("🎧 Transcribing...")
        
        transcript = await transcribe_audio(temp_file_path)
        
        await status_message.edit_text("✅ Transcription complete!")
        
        await message.reply_text(
            f"📝 Transcript:\n\n{transcript}",
            reply_to_message_id=message_id
        )
        
        delete_after = storage.get_chat_setting(chat_id, 'delete_after_transcription', True)
        
        if delete_after:
            try:
                await message.delete()
                logger.info(f"Deleted source message {message_id}")
            except TelegramError as e:
                logger.warning(f"Could not delete message {message_id}: {e}")
        
        storage.mark_processed(message_id)
        
    except Exception as e:
        error_msg = f"❌ Error processing audio: {str(e)}"
        logger.error(f"Error processing message {message_id}: {e}", exc_info=True)
        
        try:
            await status_message.edit_text(error_msg)
        except:
            await message.reply_text(error_msg)
    
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
                logger.info(f"Cleaned up temp file: {temp_file_path}")
            except Exception as e:
                logger.error(f"Error removing temp file {temp_file_path}: {e}")
        
        if temp_dir and os.path.exists(temp_dir):
            try:
                os.rmdir(temp_dir)
                logger.info(f"Cleaned up temp directory: {temp_dir}")
            except Exception as e:
                logger.error(f"Error removing temp directory {temp_dir}: {e}")

async def recover_pending_updates(application: Application):
    """Recover pending configuration instructions from recent bot history."""
    try:
        logger.info("Recovering pending updates...")
        
        updates = await application.bot.get_updates(limit=100, timeout=10)
        
        if updates:
            logger.info(f"Found {len(updates)} pending updates")
            
            for update in updates:
                if update.message and update.message.text:
                    logger.info(f"Pending message: {update.message.text[:50]}")
        else:
            logger.info("No pending updates found")
    
    except Exception as e:
        logger.warning(f"Could not recover pending updates: {e}")

async def post_init(application: Application):
    """Post-initialization hook to recover pending updates."""
    await recover_pending_updates(application)
    logger.info("Bot initialization complete")

def main():
    """Start the bot."""
    logger.info("Starting audio transcription bot...")
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("delete_on", delete_on_command))
    application.add_handler(CommandHandler("delete_off", delete_off_command))
    
    application.add_handler(MessageHandler(
        filters.VOICE | filters.AUDIO | filters.VIDEO_NOTE,
        handle_audio_message
    ))
    
    application.post_init = post_init
    
    logger.info("Bot handlers registered, starting polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    keep_alive()
    main()
