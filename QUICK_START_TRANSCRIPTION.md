# Quick Start Guide: Transcription API

## 1. Basic Setup

### Install Dependencies

```bash
uv pip install openai
```

### Set Environment Variables

```bash
# Required for bot
export BOT_TOKEN="your_telegram_bot_token"

# Optional for transcription (mock mode if not set)
export OPENAI_API_KEY="sk-your_openai_api_key"
```

## 2. Basic Usage

### Simple Transcription

```python
from transcription import transcribe_audio

# Transcribe a file
result = await transcribe_audio("audio.mp3")
print(result.text)
```

### Check if API is Configured

```python
from transcription import is_api_configured

if is_api_configured():
    print("Real transcription available")
else:
    print("Using mock mode")
```

### Safe Mode (No Exceptions)

```python
from transcription import transcribe_audio_safe

result = await transcribe_audio_safe("audio.mp3")
if result:
    print(result.text)
else:
    print("Transcription failed")
```

## 3. Add to Your Bot

### Option 1: Quick Integration

```python
from integration_example import setup_transcription_handlers

# In your main() function:
application = Application.builder().token(BOT_TOKEN).build()
setup_transcription_handlers(application)  # Add this line
application.run_polling()
```

### Option 2: Custom Handler

```python
from transcription import transcribe_audio, TranscriptionError

async def voice_handler(update: Update, context: CallbackContext):
    voice = update.message.voice
    file = await voice.get_file()
    await file.download_to_drive("voice.ogg")
    
    try:
        result = await transcribe_audio("voice.ogg")
        await update.message.reply_text(f"📝 {result.text}")
    except TranscriptionError as e:
        await update.message.reply_text(f"Error: {e}")
    finally:
        Path("voice.ogg").unlink()

# Add to your app
application.add_handler(MessageHandler(filters.VOICE, voice_handler))
```

## 4. Common Patterns

### With Language Hint

```python
# Spanish audio
result = await transcribe_audio("audio.mp3", language="es")

# French audio
result = await transcribe_audio("audio.mp3", language="fr")
```

### With Timeout

```python
# Long audio file (10 minutes timeout)
result = await transcribe_audio("long_audio.mp3", timeout=600)
```

### Error Handling

```python
from transcription import (
    transcribe_audio,
    UnsupportedFormatError,
    TranscriptionTimeoutError,
    APIKeyMissingError,
)

try:
    result = await transcribe_audio("audio.mp3")
except FileNotFoundError:
    print("File not found")
except UnsupportedFormatError:
    print("Format not supported (use MP3, WAV, M4A)")
except TranscriptionTimeoutError:
    print("Transcription timed out")
except APIKeyMissingError:
    print("API key not configured")
```

## 5. Testing

### Run Unit Tests

```bash
python test_transcription.py
```

### Test in Mock Mode

```python
# Force mock mode (even if API key is set)
result = await transcribe_audio("audio.mp3", use_mock=True)
print(result.text)  # Mock transcription
print(result.metadata['mock'])  # True
```

## 6. Metadata

The transcription result includes useful metadata:

```python
result = await transcribe_audio("audio.mp3")

print(result.text)  # Transcribed text
print(result.metadata['language'])  # Detected language
print(result.metadata['duration'])  # Duration in seconds
print(result.metadata['file_name'])  # File name
print(result.metadata['file_size'])  # File size in bytes
```

## 7. Supported Formats

- MP3 (`.mp3`)
- MP4 (`.mp4`, `.m4a`)
- MPEG (`.mpeg`, `.mpga`)
- WAV (`.wav`)
- WebM (`.webm`)

## 8. Complete Bot Example

```python
from telegram.ext import Application, MessageHandler, filters
from transcription import transcribe_audio_safe
from config import get_bot_token

async def handle_voice(update, context):
    """Transcribe voice messages."""
    voice = update.message.voice
    await update.message.reply_text("🎤 Transcribing...")
    
    file = await voice.get_file()
    path = f"voice_{voice.file_id}.ogg"
    await file.download_to_drive(path)
    
    result = await transcribe_audio_safe(path)
    
    if result:
        await update.message.reply_text(f"📝 {result.text}")
    else:
        await update.message.reply_text("❌ Transcription failed")
    
    Path(path).unlink()

# Setup
app = Application.builder().token(get_bot_token()).build()
app.add_handler(MessageHandler(filters.VOICE, handle_voice))
app.run_polling()
```

## 9. Tips

- **Mock Mode**: Automatically enabled when no API key is set
- **Cleanup**: Always delete temporary audio files after processing
- **Timeouts**: Increase for long audio files (default: 300s)
- **Language**: Provide language hint for better accuracy
- **Safe Mode**: Use `transcribe_audio_safe()` to avoid exception handling

## 10. Troubleshooting

### "API key not configured"
```bash
export OPENAI_API_KEY="sk-..."
```

### "Unsupported format"
Convert to MP3:
```bash
ffmpeg -i input.ogg output.mp3
```

### Timeout on long files
```python
result = await transcribe_audio("long.mp3", timeout=900)  # 15 min
```

## More Information

- Full API docs: `TRANSCRIPTION_API.md`
- Implementation details: `IMPLEMENTATION_SUMMARY.md`
- Usage examples: `example_transcription_usage.py`
- Integration examples: `integration_example.py`
- Unit tests: `test_transcription.py`
