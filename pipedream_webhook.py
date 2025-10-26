"""
Pipedream component for Telegram bot webhook handler.

This component receives webhook POST requests from Telegram and processes them.
It handles YouTube audio downloads and audio transcription.

Setup Instructions:
1. Create a new Python workflow in Pipedream
2. Use this code as a Python Code step
3. Set BOT_TOKEN in environment secrets
4. Deploy and copy the webhook URL
5. Set the webhook URL with Telegram: 
   https://api.telegram.org/bot<TOKEN>/setWebhook?url=<PIPEDREAM_URL>
"""

import os
import logging
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def process_webhook(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main webhook processor for Telegram updates.
    
    Args:
        event: Pipedream event containing the webhook payload
        
    Returns:
        Response dict with status and message
    """
    try:
        # Import telegram bot library
        from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
        import yt_dlp
        
        # Get bot token from environment
        bot_token = os.environ.get('BOT_TOKEN')
        if not bot_token:
            logger.error("BOT_TOKEN not found in environment variables")
            return {"statusCode": 500, "body": "Configuration error"}
        
        # Create bot instance
        bot = Bot(token=bot_token)
        
        # Parse the update from Telegram
        body = event.get('body', {})
        if not body:
            logger.warning("Empty webhook body received")
            return {"statusCode": 400, "body": "Empty body"}
        
        # Create Update object
        update = Update.de_json(body, bot)
        if not update:
            logger.warning("Failed to parse update")
            return {"statusCode": 400, "body": "Invalid update"}
        
        logger.info(f"Processing update: {update.update_id}")
        
        # Route to appropriate handler
        if update.message:
            if update.message.text:
                if update.message.text.startswith('/start'):
                    await handle_start(bot, update)
                elif update.message.text.lower() == "change" or "change" in update.message.text.lower():
                    await handle_change_command(bot, update)
                elif 'youtube.com' in update.message.text or 'youtu.be' in update.message.text:
                    await handle_youtube_download(bot, update)
                else:
                    await bot.send_message(
                        chat_id=update.message.chat_id,
                        text='Please send a valid YouTube link!'
                    )
            elif update.message.audio or update.message.voice:
                await handle_audio_transcription(bot, update)
        
        elif update.callback_query:
            await handle_callback_query(bot, update)
        
        return {"statusCode": 200, "body": "OK"}
        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        return {"statusCode": 500, "body": f"Error: {str(e)}"}


async def handle_start(bot: Bot, update: Update) -> None:
    """Handle /start command."""
    await bot.send_message(
        chat_id=update.message.chat_id,
        text=(
            'Hi! I can help you with:\n'
            '🎵 Send me a YouTube link and I\'ll convert it to MP3\n'
            '🎤 Send me a voice message or audio file and I\'ll transcribe it\n\n'
            'All transcription happens locally on the server - no external APIs needed!'
        )
    )
    logger.info(f"Sent /start response to chat {update.message.chat_id}")


async def handle_change_command(bot: Bot, update: Update) -> None:
    """Handle settings change command."""
    # Note: Settings are simplified for Pipedream - you may want to use Pipedream Data Stores
    await bot.send_message(
        chat_id=update.message.chat_id,
        text="Settings management is simplified in webhook mode. Files are deleted after processing by default."
    )


async def handle_callback_query(bot: Bot, update: Update) -> None:
    """Handle callback queries from inline keyboards."""
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith('delete_'):
        await bot.send_message(
            chat_id=query.message.chat_id,
            text="✅ Settings updated."
        )


async def handle_youtube_download(bot: Bot, update: Update) -> None:
    """Download YouTube video as MP3."""
    import yt_dlp
    
    url = update.message.text
    chat_id = update.message.chat_id
    
    # Validate YouTube URL
    if 'youtube.com' not in url and 'youtu.be' not in url:
        await bot.send_message(
            chat_id=chat_id,
            text='Please send a valid YouTube link!'
        )
        return
    
    # Send status message
    status_msg = await bot.send_message(
        chat_id=chat_id,
        text='Downloading... ⏳'
    )
    
    temp_file = None
    mp3_file = None
    
    try:
        # Create temp directory in /tmp
        temp_dir = Path('/tmp/telegram_bot')
        temp_dir.mkdir(exist_ok=True)
        
        # Configure yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': str(temp_dir / '%(title)s.%(ext)s'),
            'quiet': True,
        }
        
        # Download the audio
        logger.info(f"Downloading YouTube audio: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            mp3_file = filename.rsplit('.', 1)[0] + '.mp3'
        
        # Update status
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=status_msg.message_id,
            text='Uploading your MP3... 📤'
        )
        
        # Send the MP3 file
        logger.info(f"Sending MP3 file to chat {chat_id}")
        with open(mp3_file, 'rb') as audio:
            await bot.send_audio(
                chat_id=chat_id,
                audio=audio
            )
        
        # Delete status message
        await bot.delete_message(
            chat_id=chat_id,
            message_id=status_msg.message_id
        )
        
        logger.info(f"Successfully processed YouTube download for chat {chat_id}")
        
    except Exception as e:
        logger.error(f"Error downloading YouTube audio: {e}", exc_info=True)
        await bot.send_message(
            chat_id=chat_id,
            text=f'Sorry, an error occurred: {str(e)}'
        )
    
    finally:
        # Clean up temporary files
        if mp3_file and os.path.exists(mp3_file):
            try:
                os.remove(mp3_file)
                logger.info(f"Cleaned up MP3 file: {mp3_file}")
            except Exception as e:
                logger.error(f"Error cleaning up MP3 file: {e}")


async def handle_audio_transcription(bot: Bot, update: Update) -> None:
    """Handle audio files and voice messages for transcription."""
    chat_id = update.message.chat_id
    
    audio_file = update.message.audio or update.message.voice
    if not audio_file:
        return
    
    # Send status message
    status_msg = await bot.send_message(
        chat_id=chat_id,
        text='Transcribing audio... ⏳'
    )
    
    temp_file_path = None
    
    try:
        # Get file from Telegram
        file = await bot.get_file(audio_file.file_id)
        file_extension = '.ogg' if update.message.voice else '.mp3'
        
        # Create temp directory
        temp_dir = Path('/tmp/telegram_bot')
        temp_dir.mkdir(exist_ok=True)
        
        temp_file_path = temp_dir / f"temp_audio_{audio_file.file_id}{file_extension}"
        
        # Download file
        await file.download_to_drive(temp_file_path)
        
        # Transcribe using faster-whisper
        logger.info(f"Transcribing audio file: {temp_file_path}")
        result = await transcribe_audio_with_whisper(str(temp_file_path))
        
        if result and result.get('text'):
            transcribed_text = result['text']
            language = result.get('language', 'unknown')
            
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=status_msg.message_id,
                text=f"📝 Transcription ({language}):\n\n{transcribed_text}"
            )
            
            logger.info(f"Transcription completed for chat {chat_id}")
        else:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=status_msg.message_id,
                text='Sorry, I could not transcribe the audio. Please try again or check if the audio is clear.'
            )
        
    except Exception as e:
        logger.error(f"Error transcribing audio: {e}", exc_info=True)
        await bot.send_message(
            chat_id=chat_id,
            text=f'Sorry, an error occurred during transcription: {str(e)}'
        )
    
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
                logger.info(f"Cleaned up audio file: {temp_file_path}")
            except Exception as e:
                logger.error(f"Error cleaning up audio file: {e}")


async def transcribe_audio_with_whisper(audio_file_path: str) -> Optional[Dict[str, Any]]:
    """
    Transcribe audio using faster-whisper.
    
    Args:
        audio_file_path: Path to audio file
        
    Returns:
        Dict with transcription text and metadata, or None on failure
    """
    try:
        from faster_whisper import WhisperModel
        
        logger.info("Loading faster-whisper model...")
        # Use base model with CPU and int8 quantization for efficiency
        model = WhisperModel("base", device="cpu", compute_type="int8")
        
        logger.info(f"Transcribing: {audio_file_path}")
        segments, info = model.transcribe(
            audio_file_path,
            beam_size=5,
            best_of=5,
            temperature=0.0
        )
        
        # Collect all segments
        text = " ".join(segment.text.strip() for segment in segments)
        
        return {
            'text': text,
            'language': info.language,
            'language_probability': info.language_probability,
            'duration': info.duration
        }
        
    except Exception as e:
        logger.error(f"Error in transcription: {e}", exc_info=True)
        return None


# Pipedream handler function
def handler(pd: "pipedream"):
    """
    Main Pipedream handler function.
    
    This function is called by Pipedream when the webhook is triggered.
    """
    # Get the event data
    event = pd.steps["trigger"]["event"]
    
    # Process the webhook asynchronously
    result = asyncio.run(process_webhook(event))
    
    # Return the result
    return result
