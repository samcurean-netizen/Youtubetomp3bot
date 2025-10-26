"""
Pipedream Python Handler for Telegram Bot Webhooks

This file contains the complete handler that can be copy-pasted into 
Pipedream's Python code step.

Instructions:
1. Create a new Pipedream workflow with HTTP/Webhook trigger
2. Add a Python code step
3. Copy this entire file into the code editor
4. Set BOT_TOKEN in environment variables
5. Deploy and set webhook URL with Telegram

Dependencies (add in Pipedream):
- python-telegram-bot>=20.0
- yt-dlp
- faster-whisper>=1.0.0
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class TelegramWebhookHandler:
    """Handler for Telegram webhook updates."""
    
    def __init__(self, bot_token: str):
        """Initialize the handler with bot token."""
        from telegram import Bot
        self.bot = Bot(token=bot_token)
        self.temp_dir = Path('/tmp/telegram_bot')
        self.temp_dir.mkdir(exist_ok=True)
    
    async def process_update(self, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a Telegram update.
        
        Args:
            update_data: The update data from Telegram webhook
            
        Returns:
            Response dict with status code and body
        """
        try:
            from telegram import Update
            
            # Create Update object
            update = Update.de_json(update_data, self.bot)
            if not update:
                logger.warning("Failed to parse update")
                return {"statusCode": 400, "body": "Invalid update"}
            
            logger.info(f"Processing update: {update.update_id}")
            
            # Route to appropriate handler
            if update.message:
                await self._handle_message(update)
            elif update.callback_query:
                await self._handle_callback_query(update)
            
            return {"statusCode": 200, "body": "OK"}
            
        except Exception as e:
            logger.error(f"Error processing update: {e}", exc_info=True)
            # Still return 200 to avoid Telegram retries
            return {"statusCode": 200, "body": f"Error: {str(e)}"}
    
    async def _handle_message(self, update):
        """Handle different types of messages."""
        message = update.message
        
        if message.text:
            await self._handle_text_message(update)
        elif message.audio or message.voice:
            await self._handle_audio_message(update)
    
    async def _handle_text_message(self, update):
        """Handle text messages."""
        text = update.message.text.strip()
        chat_id = update.message.chat_id
        
        if text.startswith('/start'):
            await self._send_start_message(chat_id)
        elif text.lower() == 'change' or 'change' in text.lower():
            await self._handle_settings_change(chat_id)
        elif 'youtube.com' in text or 'youtu.be' in text:
            await self._download_youtube_audio(update, text)
        else:
            await self.bot.send_message(
                chat_id=chat_id,
                text='Please send a valid YouTube link!'
            )
    
    async def _send_start_message(self, chat_id: int):
        """Send /start message."""
        await self.bot.send_message(
            chat_id=chat_id,
            text=(
                'Hi! I can help you with:\n'
                '🎵 Send me a YouTube link and I\'ll convert it to MP3\n'
                '🎤 Send me a voice message or audio file and I\'ll transcribe it\n\n'
                'All transcription happens locally - no external APIs needed!'
            )
        )
        logger.info(f"Sent /start response to chat {chat_id}")
    
    async def _handle_settings_change(self, chat_id: int):
        """Handle settings change request."""
        await self.bot.send_message(
            chat_id=chat_id,
            text="ℹ️ In webhook mode, files are automatically deleted after processing to conserve resources."
        )
    
    async def _download_youtube_audio(self, update, url: str):
        """Download YouTube video and convert to MP3."""
        import yt_dlp
        
        chat_id = update.message.chat_id
        
        # Validate URL
        if 'youtube.com' not in url and 'youtu.be' not in url:
            await self.bot.send_message(
                chat_id=chat_id,
                text='❌ Please send a valid YouTube link!'
            )
            return
        
        # Send status message
        status_msg = await self.bot.send_message(
            chat_id=chat_id,
            text='⏳ Downloading...'
        )
        
        mp3_file = None
        
        try:
            # Configure yt-dlp
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': str(self.temp_dir / '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
            }
            
            # Download
            logger.info(f"Downloading: {url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                mp3_file = filename.rsplit('.', 1)[0] + '.mp3'
            
            # Update status
            await self.bot.edit_message_text(
                chat_id=chat_id,
                message_id=status_msg.message_id,
                text='📤 Uploading MP3...'
            )
            
            # Send file
            logger.info(f"Sending MP3: {mp3_file}")
            with open(mp3_file, 'rb') as audio:
                await self.bot.send_audio(
                    chat_id=chat_id,
                    audio=audio,
                    title=info.get('title', 'Audio')
                )
            
            # Delete status message
            await self.bot.delete_message(
                chat_id=chat_id,
                message_id=status_msg.message_id
            )
            
            logger.info(f"✅ Successfully processed YouTube download for chat {chat_id}")
            
        except Exception as e:
            logger.error(f"❌ Error downloading YouTube audio: {e}", exc_info=True)
            try:
                await self.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=status_msg.message_id,
                    text=f'❌ Sorry, an error occurred: {str(e)[:200]}'
                )
            except:
                await self.bot.send_message(
                    chat_id=chat_id,
                    text=f'❌ Sorry, an error occurred: {str(e)[:200]}'
                )
        
        finally:
            # Clean up
            if mp3_file and os.path.exists(mp3_file):
                try:
                    os.remove(mp3_file)
                    logger.info(f"🗑️ Cleaned up: {mp3_file}")
                except Exception as e:
                    logger.error(f"Error cleaning up file: {e}")
    
    async def _handle_audio_message(self, update):
        """Handle audio and voice messages for transcription."""
        chat_id = update.message.chat_id
        audio_file = update.message.audio or update.message.voice
        
        if not audio_file:
            return
        
        # Send status
        status_msg = await self.bot.send_message(
            chat_id=chat_id,
            text='⏳ Transcribing audio...'
        )
        
        temp_file = None
        
        try:
            # Download file
            file = await self.bot.get_file(audio_file.file_id)
            file_extension = '.ogg' if update.message.voice else '.mp3'
            temp_file = self.temp_dir / f"audio_{audio_file.file_id}{file_extension}"
            
            await file.download_to_drive(temp_file)
            
            # Transcribe
            logger.info(f"Transcribing: {temp_file}")
            result = await self._transcribe_audio(str(temp_file))
            
            if result and result.get('text'):
                text = result['text']
                language = result.get('language', 'unknown')
                
                # Send transcription (split if too long)
                max_length = 4000
                if len(text) <= max_length:
                    await self.bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=status_msg.message_id,
                        text=f"📝 Transcription ({language}):\n\n{text}"
                    )
                else:
                    # Send in chunks
                    await self.bot.delete_message(chat_id=chat_id, message_id=status_msg.message_id)
                    chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
                    for i, chunk in enumerate(chunks):
                        header = f"📝 Transcription ({language}) - Part {i+1}/{len(chunks)}:\n\n" if len(chunks) > 1 else f"📝 Transcription ({language}):\n\n"
                        await self.bot.send_message(
                            chat_id=chat_id,
                            text=header + chunk
                        )
                
                logger.info(f"✅ Transcription completed for chat {chat_id}")
            else:
                await self.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=status_msg.message_id,
                    text='❌ Sorry, I could not transcribe the audio. Please try again.'
                )
            
        except Exception as e:
            logger.error(f"❌ Error transcribing audio: {e}", exc_info=True)
            try:
                await self.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=status_msg.message_id,
                    text=f'❌ Sorry, an error occurred: {str(e)[:200]}'
                )
            except:
                await self.bot.send_message(
                    chat_id=chat_id,
                    text=f'❌ Sorry, an error occurred: {str(e)[:200]}'
                )
        
        finally:
            # Clean up
            if temp_file and os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                    logger.info(f"🗑️ Cleaned up: {temp_file}")
                except Exception as e:
                    logger.error(f"Error cleaning up file: {e}")
    
    async def _transcribe_audio(self, audio_path: str) -> Optional[Dict[str, Any]]:
        """
        Transcribe audio using faster-whisper.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Dict with transcription results or None on failure
        """
        try:
            from faster_whisper import WhisperModel
            import asyncio
            
            logger.info("Loading Whisper model...")
            
            # Load model (will be cached after first use)
            loop = asyncio.get_event_loop()
            model = await loop.run_in_executor(
                None,
                lambda: WhisperModel("base", device="cpu", compute_type="int8")
            )
            
            logger.info(f"Transcribing audio: {audio_path}")
            
            # Transcribe
            segments_gen, info = await loop.run_in_executor(
                None,
                lambda: model.transcribe(
                    audio_path,
                    beam_size=5,
                    best_of=5,
                    temperature=0.0
                )
            )
            
            # Collect segments
            segments = list(segments_gen)
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
    
    async def _handle_callback_query(self, update):
        """Handle callback queries from inline keyboards."""
        query = update.callback_query
        await query.answer()
        
        # For future use - currently simplified
        await self.bot.send_message(
            chat_id=query.message.chat_id,
            text="✅ Setting updated."
        )


# Main handler function for Pipedream
async def handler(pd: "pipedream"):
    """
    Main Pipedream handler function.
    
    This function is called by Pipedream when the webhook is triggered.
    
    Args:
        pd: Pipedream context object
        
    Returns:
        Response dict with status code and body
    """
    import asyncio
    
    # Get bot token from environment
    bot_token = os.environ.get('BOT_TOKEN')
    if not bot_token:
        logger.error("BOT_TOKEN not found in environment variables")
        return {"statusCode": 500, "body": "Configuration error: BOT_TOKEN not set"}
    
    # Get the webhook payload
    try:
        event = pd.steps["trigger"]["event"]
        update_data = event.get("body", {})
        
        if not update_data:
            logger.warning("Empty webhook body")
            return {"statusCode": 400, "body": "Empty body"}
        
        # Process the update
        webhook_handler = TelegramWebhookHandler(bot_token)
        result = await webhook_handler.process_update(update_data)
        
        return result
        
    except Exception as e:
        logger.error(f"Fatal error in handler: {e}", exc_info=True)
        return {"statusCode": 500, "body": f"Error: {str(e)}"}


# For local testing
if __name__ == "__main__":
    import asyncio
    import json
    
    # Mock Pipedream context for local testing
    class MockPD:
        steps = {
            "trigger": {
                "event": {
                    "body": {
                        "update_id": 123456789,
                        "message": {
                            "message_id": 1,
                            "from": {"id": 123, "first_name": "Test"},
                            "chat": {"id": 123, "type": "private"},
                            "text": "/start"
                        }
                    }
                }
            }
        }
    
    # Run test
    print("Testing handler locally...")
    result = asyncio.run(handler(MockPD()))
    print(f"Result: {json.dumps(result, indent=2)}")
