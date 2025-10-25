"""Integration example showing how to add transcription to the Telegram bot.

This file demonstrates how to integrate the transcription API into main.py
for handling voice messages and audio files.
"""
import os
import logging
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

from config import get_bot_token, get_openai_api_key
from transcription import (
    transcribe_audio,
    transcribe_audio_safe,
    is_api_configured,
    TranscriptionError,
    UnsupportedFormatError,
    TranscriptionTimeoutError,
    APIKeyMissingError,
)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


async def transcribe_command(update: Update, context: CallbackContext):
    """Handle /transcribe command to check if transcription is available."""
    if is_api_configured():
        await update.message.reply_text(
            '✅ Transcription service is active!\n\n'
            'Send me a voice message or audio file and I\'ll transcribe it for you.'
        )
    else:
        await update.message.reply_text(
            '⚠️ Transcription service is in mock mode (API key not configured).\n\n'
            'You can still send audio files, but transcriptions will be mock responses.'
        )


async def handle_voice_message(update: Update, context: CallbackContext):
    """Handle voice messages and transcribe them."""
    voice = update.message.voice
    
    if not voice:
        return
    
    await update.message.reply_text('🎤 Transcribing your voice message...')
    
    try:
        voice_file = await voice.get_file()
        file_path = f"voice_{voice.file_id}.ogg"
        await voice_file.download_to_drive(file_path)
        
        result = await transcribe_audio(file_path, timeout=180)
        
        response = f"📝 **Transcription:**\n{result.text}\n\n"
        
        if result.metadata.get('mock'):
            response += "⚠️ _Using mock transcription (API key not configured)_\n"
        
        if result.metadata.get('language'):
            response += f"🌍 Language: {result.metadata['language']}\n"
        
        if result.metadata.get('duration'):
            duration = result.metadata['duration']
            response += f"⏱️ Duration: {duration:.1f}s\n"
        
        await update.message.reply_text(response)
        
    except FileNotFoundError:
        await update.message.reply_text('❌ Voice file not found.')
    
    except UnsupportedFormatError as e:
        await update.message.reply_text(
            f'❌ Unsupported audio format.\n\n'
            f'Please use: MP3, WAV, M4A, or WebM.'
        )
    
    except TranscriptionTimeoutError:
        await update.message.reply_text(
            '⏱️ Transcription timed out. Please try with a shorter audio clip.'
        )
    
    except APIKeyMissingError:
        await update.message.reply_text(
            '❌ Transcription service is not configured.\n'
            'Please contact the bot administrator.'
        )
    
    except TranscriptionError as e:
        logger.error(f"Transcription error: {e}", exc_info=True)
        await update.message.reply_text(
            f'❌ Transcription failed: {str(e)}'
        )
    
    finally:
        if Path(file_path).exists():
            Path(file_path).unlink()


async def handle_audio_file(update: Update, context: CallbackContext):
    """Handle audio files and transcribe them."""
    audio = update.message.audio
    
    if not audio:
        return
    
    await update.message.reply_text('🎵 Transcribing your audio file...')
    
    file_path = None
    
    try:
        audio_file = await audio.get_file()
        file_name = audio.file_name or f"audio_{audio.file_id}.mp3"
        file_path = file_name
        await audio_file.download_to_drive(file_path)
        
        language_hint = None
        if context.args:
            language_hint = context.args[0]
        
        result = await transcribe_audio(
            file_path,
            language=language_hint,
            timeout=300
        )
        
        response = f"📝 **Transcription:**\n{result.text}\n\n"
        response += f"📄 File: {audio.file_name or 'Unknown'}\n"
        
        if result.metadata.get('mock'):
            response += "⚠️ _Using mock transcription (API key not configured)_\n"
        
        if result.metadata.get('language'):
            response += f"🌍 Language: {result.metadata['language']}\n"
        
        if result.metadata.get('duration'):
            duration = result.metadata['duration']
            response += f"⏱️ Duration: {duration:.1f}s\n"
        
        if audio.file_size:
            size_mb = audio.file_size / (1024 * 1024)
            response += f"💾 Size: {size_mb:.2f} MB\n"
        
        await update.message.reply_text(response)
        
    except UnsupportedFormatError:
        await update.message.reply_text(
            '❌ Unsupported audio format.\n\n'
            'Supported formats: MP3, MP4, WAV, M4A, WebM'
        )
    
    except TranscriptionTimeoutError:
        await update.message.reply_text(
            '⏱️ Transcription timed out. The file might be too long.'
        )
    
    except TranscriptionError as e:
        logger.error(f"Transcription error: {e}", exc_info=True)
        await update.message.reply_text(
            f'❌ Transcription failed: {str(e)}'
        )
    
    finally:
        if file_path and Path(file_path).exists():
            Path(file_path).unlink()


async def handle_youtube_with_transcription(update: Update, context: CallbackContext):
    """Enhanced YouTube handler that also transcribes the audio."""
    import yt_dlp
    
    url = update.message.text
    
    if 'youtube.com' not in url and 'youtu.be' not in url:
        await update.message.reply_text('Please send a valid YouTube link!')
        return
    
    await update.message.reply_text('⏳ Downloading audio...')
    
    mp3_file = None
    
    try:
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
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            mp3_file = filename.rsplit('.', 1)[0] + '.mp3'
        
        await update.message.reply_text('📤 Uploading MP3...')
        
        with open(mp3_file, 'rb') as audio:
            await update.message.reply_audio(audio=audio)
        
        if is_api_configured() or True:
            await update.message.reply_text('📝 Transcribing audio...')
            
            result = await transcribe_audio_safe(mp3_file, timeout=600)
            
            if result:
                transcription_msg = f"📝 **Transcription:**\n\n{result.text[:4000]}"
                
                if len(result.text) > 4000:
                    transcription_msg += "\n\n_[Truncated - transcription too long]_"
                
                if result.metadata.get('mock'):
                    transcription_msg += "\n\n⚠️ _Mock transcription (API not configured)_"
                
                await update.message.reply_text(transcription_msg)
            else:
                await update.message.reply_text(
                    '⚠️ Could not transcribe audio.'
                )
        
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        await update.message.reply_text(f'❌ Error: {str(e)}')
    
    finally:
        if mp3_file and os.path.exists(mp3_file):
            os.remove(mp3_file)


def setup_transcription_handlers(application: Application):
    """
    Add transcription-related handlers to the bot application.
    
    Usage:
        application = Application.builder().token(BOT_TOKEN).build()
        setup_transcription_handlers(application)
    """
    application.add_handler(CommandHandler("transcribe", transcribe_command))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice_message))
    application.add_handler(MessageHandler(filters.AUDIO, handle_audio_file))


if __name__ == '__main__':
    print("=" * 60)
    print("Integration Example - Transcription API")
    print("=" * 60)
    print("\nThis file demonstrates how to integrate transcription features")
    print("into your Telegram bot. Key points:\n")
    print("1. Import transcription functions from transcription.py")
    print("2. Use is_api_configured() to check if API is available")
    print("3. Use transcribe_audio() for transcription with error handling")
    print("4. Use transcribe_audio_safe() for no-exception mode")
    print("5. Handle all TranscriptionError exceptions appropriately")
    print("6. Clean up temporary files in finally blocks")
    print("\nHandlers included:")
    print("  - /transcribe: Check transcription service status")
    print("  - Voice messages: Automatic transcription")
    print("  - Audio files: Transcription with language hints")
    print("  - YouTube URLs: Download + transcribe")
    print("\nTo use in main.py:")
    print("  from integration_example import setup_transcription_handlers")
    print("  setup_transcription_handlers(application)")
    print("=" * 60)
