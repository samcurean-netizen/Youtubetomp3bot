# Audio Transcription Telegram Bot

An async Telegram bot built with python-telegram-bot v20 that transcribes audio messages, voice notes, and video notes.

## Features

- 🎤 Transcribe voice messages
- 🎵 Transcribe audio files
- 🎥 Transcribe video notes
- 🔄 Automatic duplicate detection
- 🗑️ Configurable audio deletion after transcription
- 👥 Works in both private chats and groups
- 🔧 Admin configuration commands
- 💾 Persistent storage for settings and processed messages
- 🌐 Built-in keep-alive web server for Replit deployment

## Setup

### Environment Variables

Required:
- `BOT_TOKEN` - Your Telegram bot token from [@BotFather](https://t.me/BotFather)

Optional:
- `ADMIN_USER_IDS` - Comma-separated list of admin user IDs (e.g., "123456789,987654321")
- `TRANSCRIPTION_API_KEY` - API key for your transcription service

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Or with uv:
   ```bash
   uv sync
   ```
3. Set environment variables
4. Run the bot:
   ```bash
   python main.py
   ```

## Usage

### User Commands

- `/start` - Display welcome message and bot capabilities

### Admin Commands

- `/status` - View current chat settings
- `/delete_on` - Enable automatic deletion of source audio after transcription (default)
- `/delete_off` - Disable automatic deletion of source audio

### Sending Audio

Simply send any of the following to the bot:
- Voice messages (recorded in Telegram)
- Audio files (uploaded files)
- Video notes (round video messages)

The bot will:
1. Download the audio
2. Transcribe it
3. Reply with the transcript
4. Delete the source message (if enabled)
5. Clean up temporary files

## Architecture

### Main Components

- **BotStorage**: Persistent JSON-based storage for:
  - Processed message IDs (prevents duplicate transcriptions)
  - Per-chat settings (delete preferences)
  - Pending configuration states

- **Audio Handler**: Async message handler that:
  - Downloads audio to temporary directory
  - Routes to transcription service
  - Sends transcript back to user
  - Handles cleanup and error recovery

- **Keep-Alive Server**: Flask web server for Replit deployment

### File Structure

```
.
├── main.py              # Main bot code
├── bot_config.json      # Persistent storage (auto-generated)
├── pyproject.toml       # Project dependencies
├── .replit              # Replit configuration
└── .gitignore           # Git ignore rules
```

## Configuration

### Per-Chat Settings

Each chat (private or group) maintains its own settings:
- `delete_after_transcription`: Whether to delete source audio (default: true)

### Global Settings

- `MAX_FILE_SIZE_MB`: Maximum file size for transcription (default: 20MB)
- `PROCESSED_IDS_LIMIT`: Maximum number of processed message IDs to track (default: 1000)

## Transcription Service Integration

The bot includes a placeholder transcription function that can be easily integrated with real services:

### Supported Services

You can integrate any transcription API:
- OpenAI Whisper API
- Google Speech-to-Text
- AWS Transcribe
- Azure Speech Services
- Assembly AI
- And more...

### Implementation

Edit the `transcribe_audio()` function in `main.py` to add your transcription service integration.

## Error Handling

The bot includes comprehensive error handling:
- File download failures
- Transcription errors
- Message deletion failures (e.g., insufficient permissions)
- Storage errors
- Network issues

All errors are logged and user-friendly error messages are sent to the user.

## Deployment

### Replit

The bot is pre-configured for Replit deployment:
1. Fork/import the repository to Replit
2. Add `BOT_TOKEN` to Secrets
3. Run the project

The keep-alive web server will automatically start on port 8080.

### Other Platforms

The bot can run on any platform that supports Python 3.11+:
- Heroku
- Railway
- DigitalOcean
- AWS EC2
- Local server

## Development

### Adding New Commands

```python
async def my_command(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello!")

# In main():
application.add_handler(CommandHandler("mycommand", my_command))
```

### Adding New Message Handlers

```python
async def my_handler(update: Update, context: CallbackContext):
    # Handle message
    pass

# In main():
application.add_handler(MessageHandler(filters.TEXT, my_handler))
```

## License

MIT

## Support

For issues and questions, please open an issue on the repository.
