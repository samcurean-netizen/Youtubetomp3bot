"""Example usage of the transcription API module.

This file demonstrates how to integrate the transcription module with the bot.
"""
import asyncio
import logging
from pathlib import Path

from transcription import (
    transcribe_audio,
    transcribe_audio_safe,
    is_api_configured,
    TranscriptionError,
    UnsupportedFormatError,
    TranscriptionTimeoutError,
    APIKeyMissingError,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def example_basic_usage():
    """Basic transcription usage."""
    audio_file = "path/to/audio.mp3"
    
    try:
        result = await transcribe_audio(audio_file)
        print(f"Transcription: {result.text}")
        print(f"Language: {result.metadata.get('language')}")
        print(f"Duration: {result.metadata.get('duration')}")
    except FileNotFoundError:
        print("Audio file not found")
    except UnsupportedFormatError as e:
        print(f"Unsupported format: {e}")
    except TranscriptionError as e:
        print(f"Transcription error: {e}")


async def example_with_language_hint():
    """Transcription with language hint."""
    audio_file = "path/to/audio.mp3"
    
    result = await transcribe_audio(audio_file, language='es')
    print(f"Spanish transcription: {result.text}")


async def example_safe_usage():
    """Safe transcription that never raises exceptions."""
    audio_file = "path/to/audio.mp3"
    
    result = await transcribe_audio_safe(audio_file, language='en', timeout=120)
    
    if result:
        print(f"Transcription: {result.text}")
    else:
        print("Transcription failed or returned no result")


async def example_telegram_bot_handler():
    """Example of how to use transcription in a Telegram bot handler."""
    from telegram import Update
    from telegram.ext import CallbackContext
    
    async def handle_voice_message(update: Update, context: CallbackContext):
        """Handle voice messages and transcribe them."""
        voice = update.message.voice
        
        if not voice:
            await update.message.reply_text("No voice message found!")
            return
        
        await update.message.reply_text("Transcribing your voice message... 🎤")
        
        voice_file = await voice.get_file()
        file_path = f"voice_{voice.file_id}.ogg"
        await voice_file.download_to_drive(file_path)
        
        try:
            result = await transcribe_audio(file_path, timeout=180)
            
            response = f"📝 Transcription:\n{result.text}\n\n"
            
            if result.metadata.get('language'):
                response += f"🌍 Language: {result.metadata['language']}\n"
            
            if result.metadata.get('duration'):
                response += f"⏱️ Duration: {result.metadata['duration']:.1f}s"
            
            await update.message.reply_text(response)
            
        except UnsupportedFormatError:
            await update.message.reply_text(
                "Sorry, this audio format is not supported. "
                "Please send in MP3, WAV, or M4A format."
            )
        except TranscriptionTimeoutError:
            await update.message.reply_text(
                "The transcription is taking too long. "
                "Please try with a shorter audio file."
            )
        except APIKeyMissingError:
            await update.message.reply_text(
                "Transcription service is not configured. "
                "Please contact the bot administrator."
            )
        except TranscriptionError as e:
            logger.error(f"Transcription error: {e}")
            await update.message.reply_text(
                f"Sorry, transcription failed: {str(e)}"
            )
        finally:
            Path(file_path).unlink(missing_ok=True)


async def example_check_api_configuration():
    """Check if API is configured before attempting transcription."""
    if is_api_configured():
        print("✓ OpenAI API is configured")
        audio_file = "path/to/audio.mp3"
        result = await transcribe_audio(audio_file)
        print(f"Transcription: {result.text}")
    else:
        print("⚠ OpenAI API key not configured")
        print("Using mock mode for development...")
        audio_file = "path/to/audio.mp3"
        result = await transcribe_audio(audio_file, use_mock=True)
        print(f"Mock transcription: {result.text}")


async def example_batch_transcription():
    """Transcribe multiple audio files."""
    audio_files = [
        "audio1.mp3",
        "audio2.mp3",
        "audio3.mp3",
    ]
    
    results = []
    
    for audio_file in audio_files:
        result = await transcribe_audio_safe(audio_file)
        
        if result:
            results.append({
                'file': audio_file,
                'text': result.text,
                'language': result.metadata.get('language'),
            })
            print(f"✓ Transcribed: {audio_file}")
        else:
            print(f"✗ Failed: {audio_file}")
    
    return results


if __name__ == '__main__':
    print("Transcription API Usage Examples")
    print("=" * 50)
    print("\nNote: These examples show how to use the API.")
    print("They won't run without actual audio files and API keys.")
    print("\nSee test_transcription.py for runnable unit tests.")
