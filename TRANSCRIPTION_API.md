# Transcription API Documentation

## Overview

The `transcription.py` module provides a clean, async-friendly wrapper around the OpenAI Whisper API for converting audio files to text. It includes robust error handling, automatic fallback to mock mode during development, and comprehensive metadata support.

## Features

- ✅ Async/await compatible for use with python-telegram-bot
- ✅ Automatic mock mode when API key is not configured
- ✅ Support for multiple audio formats (MP3, MP4, WAV, M4A, WebM, etc.)
- ✅ Optional language hints for better accuracy
- ✅ Configurable timeouts
- ✅ Comprehensive error handling with custom exceptions
- ✅ Detailed metadata in responses (language, duration, segments)
- ✅ Unit-testable with mock responses
- ✅ File streaming for memory efficiency
- ✅ Environment variable configuration via config helpers

## Installation

Add the OpenAI package to your dependencies:

```bash
pip install openai>=1.0.0
```

Or update your `pyproject.toml`:

```toml
dependencies = [
    "openai>=1.0.0",
]
```

## Configuration

Set the OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="sk-..."
```

If the API key is not set, the module automatically uses mock mode for development.

## Basic Usage

### Simple Transcription

```python
from transcription import transcribe_audio

# Transcribe an audio file
result = await transcribe_audio("audio.mp3")
print(result.text)  # Transcribed text
```

### With Language Hint

```python
# Provide language hint for better accuracy
result = await transcribe_audio("audio.mp3", language="es")
print(result.text)
print(result.metadata['language'])  # 'es'
```

### With Custom Timeout

```python
# Set custom timeout (default: 300 seconds)
result = await transcribe_audio("long_audio.mp3", timeout=600)
```

### Safe Mode (No Exceptions)

```python
from transcription import transcribe_audio_safe

# Returns None on failure instead of raising exceptions
result = await transcribe_audio_safe("audio.mp3")
if result:
    print(result.text)
else:
    print("Transcription failed")
```

## API Reference

### Main Functions

#### `transcribe_audio()`

```python
async def transcribe_audio(
    audio_file_path: str,
    language: Optional[str] = None,
    timeout: int = 300,
    use_mock: Optional[bool] = None
) -> TranscriptionResult
```

Transcribe an audio file using OpenAI Whisper API.

**Parameters:**
- `audio_file_path` (str): Path to audio file on disk
- `language` (Optional[str]): ISO-639-1 language code (e.g., 'en', 'es', 'fr')
- `timeout` (int): Timeout in seconds for API request (default: 300)
- `use_mock` (Optional[bool]): Force mock mode. If None, auto-detect based on API key

**Returns:**
- `TranscriptionResult`: Object containing transcribed text and metadata

**Raises:**
- `FileNotFoundError`: Audio file doesn't exist
- `UnsupportedFormatError`: Audio format not supported
- `TranscriptionTimeoutError`: Request timed out
- `TranscriptionAPIError`: API returned an error
- `APIKeyMissingError`: API key missing and mock mode disabled

#### `transcribe_audio_safe()`

```python
async def transcribe_audio_safe(
    audio_file_path: str,
    language: Optional[str] = None,
    timeout: int = 300
) -> Optional[TranscriptionResult]
```

Safely transcribe audio with automatic fallback to mock mode. Never raises exceptions.

**Returns:**
- `TranscriptionResult` on success, `None` on failure

#### `is_api_configured()`

```python
def is_api_configured() -> bool
```

Check if OpenAI API key is configured.

**Returns:**
- `True` if API key is available, `False` otherwise

### Data Classes

#### `TranscriptionResult`

Container for transcription results.

**Attributes:**
- `text` (str): The transcribed text
- `metadata` (Dict[str, Any]): Additional information
  - `language` (str): Detected or specified language
  - `duration` (float): Audio duration in seconds
  - `file_name` (str): Original file name
  - `file_size` (int): File size in bytes
  - `segments` (List): Detailed segment information (if available)
  - `mock` (bool): True if using mock mode

**Methods:**
- `__str__()`: Returns the transcribed text
- `__repr__()`: Returns detailed representation

### Exception Classes

All exceptions inherit from `TranscriptionError`:

- `TranscriptionError`: Base exception for all transcription errors
- `APIKeyMissingError`: API key not configured
- `UnsupportedFormatError`: Audio format not supported
- `TranscriptionTimeoutError`: Request timed out
- `TranscriptionAPIError`: API error occurred

### Supported Audio Formats

- MP3 (`.mp3`)
- MP4 (`.mp4`, `.m4a`)
- MPEG (`.mpeg`, `.mpga`)
- WAV (`.wav`)
- WebM (`.webm`)

## Integration Examples

### Telegram Bot Handler

```python
from telegram import Update
from telegram.ext import CallbackContext
from transcription import transcribe_audio, TranscriptionError

async def voice_handler(update: Update, context: CallbackContext):
    """Handle voice messages."""
    voice = update.message.voice
    
    # Download voice message
    file = await voice.get_file()
    file_path = f"voice_{voice.file_id}.ogg"
    await file.download_to_drive(file_path)
    
    try:
        # Transcribe
        result = await transcribe_audio(file_path, language='en')
        
        # Send result
        await update.message.reply_text(
            f"📝 Transcription:\n{result.text}"
        )
    except TranscriptionError as e:
        await update.message.reply_text(f"Error: {e}")
    finally:
        # Clean up
        Path(file_path).unlink(missing_ok=True)
```

### YouTube Audio Transcription

```python
import yt_dlp
from transcription import transcribe_audio

async def transcribe_youtube(url: str):
    """Download and transcribe YouTube video."""
    
    # Download audio
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'outtmpl': 'audio.%(ext)s',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    # Transcribe
    result = await transcribe_audio('audio.mp3')
    
    return result.text
```

### Batch Processing

```python
from pathlib import Path
from transcription import transcribe_audio_safe

async def transcribe_directory(directory: str):
    """Transcribe all audio files in a directory."""
    results = []
    
    for audio_file in Path(directory).glob('*.mp3'):
        result = await transcribe_audio_safe(str(audio_file))
        
        if result:
            results.append({
                'file': audio_file.name,
                'text': result.text,
                'language': result.metadata.get('language'),
            })
    
    return results
```

## Development & Testing

### Mock Mode

When the OpenAI API key is not configured, the module automatically enters mock mode:

```python
# No API key set - automatically uses mock
result = await transcribe_audio("audio.mp3")
print(result.text)  # "This is a mock transcription..."
print(result.metadata['mock'])  # True
```

You can also force mock mode:

```python
result = await transcribe_audio("audio.mp3", use_mock=True)
```

### Running Tests

```bash
# Run unit tests
python test_transcription.py

# With pytest
pytest test_transcription.py
```

### Test Coverage

The module includes comprehensive unit tests:
- ✅ Mock transcription
- ✅ Language hints
- ✅ File validation
- ✅ Format validation
- ✅ Error handling
- ✅ Safe mode
- ✅ All supported formats

## Configuration Module

The `config.py` module provides helpers for loading environment variables:

```python
from config import get_openai_api_key, get_bot_token, get_env_var

# Get API keys
api_key = get_openai_api_key()  # Returns None if not set
bot_token = get_bot_token()  # Raises ValueError if not set

# Custom environment variables
custom = get_env_var('CUSTOM_VAR', default='default_value')
required = get_env_var('REQUIRED_VAR', required=True)
```

## Error Handling Best Practices

### Option 1: Catch Specific Exceptions

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
    print("Format not supported")
except TranscriptionTimeoutError:
    print("Request timed out")
except APIKeyMissingError:
    print("API key not configured")
```

### Option 2: Catch All Transcription Errors

```python
from transcription import transcribe_audio, TranscriptionError

try:
    result = await transcribe_audio("audio.mp3")
except TranscriptionError as e:
    print(f"Transcription failed: {e}")
```

### Option 3: Use Safe Mode

```python
from transcription import transcribe_audio_safe

result = await transcribe_audio_safe("audio.mp3")
if result:
    print(result.text)
else:
    print("Failed")
```

## Performance Considerations

- **Streaming**: Files are streamed to the API for memory efficiency
- **Timeouts**: Default 300s timeout prevents hanging on large files
- **Async**: Fully async for non-blocking operation
- **Clean-up**: Remember to delete temporary audio files after transcription

## Troubleshooting

### API Key Not Working

```python
from transcription import is_api_configured

if not is_api_configured():
    print("Set OPENAI_API_KEY environment variable")
```

### Unsupported Format

Convert audio to supported format first:

```bash
ffmpeg -i input.ogg output.mp3
```

### Timeout Issues

Increase timeout for large files:

```python
result = await transcribe_audio("large_file.mp3", timeout=600)
```

## License

Part of the Telegram bot project.
