# Telegram Audio Bot

A powerful Telegram bot that handles YouTube audio downloads and local speech-to-text transcription.

## Features

- 🎵 **YouTube to MP3**: Send a YouTube link and get an MP3 file back
- 🎤 **Audio Transcription**: Send voice messages or audio files for local transcription
- 💾 **Smart Storage**: Configurable file deletion after processing
- 👥 **Group Support**: Works in private chats and groups with admin controls
- 🔒 **Privacy First**: All transcription happens locally - no external APIs needed
- 📊 **Database Tracking**: Prevents duplicate processing of messages and audio files

## Requirements

- Python 3.11+
- FFmpeg (for audio processing)
- Telegram Bot Token

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
# or using uv (recommended):
uv pip install -e .
```

3. Install FFmpeg (if not already installed):
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

4. Set up your Telegram Bot Token:
   - Talk to [@BotFather](https://t.me/botfather) on Telegram
   - Create a new bot or use an existing one
   - Copy the bot token

5. Set the environment variable:
```bash
export BOT_TOKEN="your-telegram-bot-token-here"
```

Or create a `.env` file (if using a tool that loads it):
```
BOT_TOKEN=your-telegram-bot-token-here
```

## Usage

### Running the Bot

```bash
python main.py
```

The bot will start and be accessible on Telegram. It also runs a Flask keep-alive server on port 8080.

### Bot Commands

- `/start` - Initialize the bot and see available features

### Features

#### YouTube to MP3
Simply send a YouTube URL to the bot (works in private chats or groups):
```
https://www.youtube.com/watch?v=example
```

The bot will:
1. Download the audio from YouTube
2. Convert it to MP3 format
3. Send the MP3 file back to you
4. Optionally delete the file based on your settings

#### Audio Transcription
Send any voice message or audio file to the bot, and it will:
1. Download the audio file
2. Transcribe it using a local Whisper model (no API calls!)
3. Send back the transcribed text with detected language
4. Optionally delete the file based on your settings

Supported audio formats:
- `.mp3`, `.mp4`, `.mpeg`, `.mpga`, `.m4a`
- `.wav`, `.webm`, `.ogg`, `.oga`
- Voice messages

#### Settings Management

Admins can control whether files are deleted after processing:

1. When you first start the bot, admins will be asked about file deletion preferences
2. To change settings later, send: `change` (or `@botname change` in groups)
3. The bot will toggle between keeping and deleting files

## Architecture

### Components

- **main.py**: Core bot logic, handlers, and Flask keep-alive server
- **database.py**: SQLite database for settings and processed message tracking
- **transcription.py**: Local audio transcription using faster-whisper

### Database Schema

The bot uses SQLite to store:
- Chat settings (deletion preferences, admin prompts)
- Processed message IDs (prevents duplicate handling)
- Processed audio file IDs (prevents reprocessing)

### Transcription Technology

The bot uses [faster-whisper](https://github.com/guillaumekln/faster-whisper), a reimplementation of OpenAI's Whisper model using CTranslate2:

- **Model**: Base model (good balance of speed and accuracy)
- **Compute**: CPU with int8 quantization for efficiency
- **Privacy**: All processing happens locally - no data sent to external APIs
- **Speed**: Significantly faster than the original Whisper implementation
- **First Run**: The model will be downloaded automatically on first use (~150MB)

## Configuration

### Environment Variables

- `BOT_TOKEN` (required): Your Telegram bot token from BotFather

### Model Selection

The transcription module uses the `base` model by default. You can modify this in `transcription.py`:

```python
# In _get_model() function:
WhisperModel("base", ...)  # Options: tiny, base, small, medium, large
```

Model comparison:
- **tiny**: Fastest, less accurate (~75MB)
- **base**: Good balance (~150MB) - **Default**
- **small**: More accurate (~500MB)
- **medium**: High accuracy (~1.5GB)
- **large**: Best accuracy (~3GB)

## Development

### Project Structure

```
.
├── main.py              # Main bot application
├── database.py          # Database operations
├── transcription.py     # Audio transcription module
├── pyproject.toml       # Project dependencies
├── README.md           # This file
└── bot_data.db         # SQLite database (created at runtime)
```

### Running in Development

The bot is designed to run continuously. For development on platforms like Replit:
- The Flask server on port 8080 helps keep the bot alive
- The server responds to health checks with "Bot is running!"

### Testing

Send test messages to your bot:
1. YouTube URLs for download testing
2. Voice messages for transcription testing
3. Admin commands in groups to test settings

## Deployment

### Replit/Cloud Platforms

1. Fork the repository to your platform
2. Set the `BOT_TOKEN` secret/environment variable
3. Run the bot

The Flask keep-alive server will help prevent the bot from sleeping on free tiers.

### VPS/Dedicated Server

1. Clone the repository
2. Set up a systemd service or use screen/tmux
3. Ensure FFmpeg is installed
4. Set environment variables
5. Run the bot

Example systemd service:
```ini
[Unit]
Description=Telegram Audio Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/bot
Environment="BOT_TOKEN=your-token-here"
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## Troubleshooting

### Model Download Issues
If the Whisper model fails to download:
- Ensure you have a stable internet connection on first run
- Check disk space (models can be 150MB - 3GB depending on size)
- The model is cached after first download

### FFmpeg Not Found
Install FFmpeg for your platform (see Installation section).

### Transcription Quality
- For better accuracy, use a larger model (edit `transcription.py`)
- Ensure audio quality is good (clear speech, minimal background noise)
- Specify language if known: `transcribe_audio(path, language="en")`

### Memory Usage
- The base model uses ~500MB RAM during transcription
- Larger models require more memory
- Consider using `tiny` model on limited hardware

## License

[Add your license here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [faster-whisper](https://github.com/guillaumekln/faster-whisper) - Fast Whisper implementation
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloader
- [OpenAI Whisper](https://github.com/openai/whisper) - Original Whisper model
