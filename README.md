# YouTube to MP3 Telegram Bot 🎵

A Telegram bot that converts YouTube videos to MP3 audio files and sends them directly to users. Built with Python, designed for easy deployment on Replit.

![Bot Icon](generated-icon.png)

## Features

- 🎬 Convert YouTube videos to MP3 audio
- 📱 Simple Telegram interface - just send a YouTube link
- 🔄 Automatic file cleanup (configurable)
- 🚀 Easy deployment on Replit with keep-alive functionality
- ⚙️ Centralized configuration with environment variables
- 📊 Logging for monitoring and debugging

## Prerequisites

Before deploying this bot, you'll need:

1. A **Telegram Bot Token** from [@BotFather](https://t.me/BotFather)
2. A **Replit account** (free tier works fine)
3. Basic familiarity with Telegram

## Quick Start on Replit

### Step 1: Fork/Import the Project

1. Log in to [Replit](https://replit.com)
2. Click **"Create Repl"** or import this repository
3. Select **Python** as the language
4. Wait for Replit to load the project

### Step 2: Get Your Telegram Bot Token

1. Open Telegram and search for **@BotFather**
2. Start a chat and send `/newbot`
3. Follow the prompts:
   - Give your bot a name (e.g., "My YouTube MP3 Bot")
   - Give your bot a username (must end with "bot", e.g., "my_yt_mp3_bot")
4. **Copy the bot token** - it looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

### Step 3: Configure Environment Variables

Environment variables in Replit are called "Secrets". Here's how to add them:

1. In your Repl, look for the **🔒 Secrets** tab in the left sidebar (Tools section)
2. If you don't see it, click the lock icon at the bottom of the left sidebar
3. Click **"New Secret"**
4. Add the following:
   - **Key**: `BOT_TOKEN`
   - **Value**: Paste your bot token from Step 2
5. Click **"Add new secret"** or press **Enter**

**Optional secrets** (for future features):
- `OPENAI_API_KEY` - If you plan to add AI features
- `DATABASE_PATH` - Custom database file path (defaults to `bot_data.db`)
- `LOG_LEVEL` - Set logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`)
- `DELETE_FILES_AFTER_SEND` - Set to `false` to keep downloaded files (defaults to `true`)

### Step 4: Install Dependencies

Replit should automatically detect and install dependencies from `pyproject.toml`. If not:

1. Open the **Shell** tab (console icon in the sidebar)
2. Run the following command:
   ```bash
   pip install -e .
   ```

### Step 5: Run the Bot

1. Click the **"Run"** button at the top of the Repl
2. Wait for the bot to start - you should see logs like:
   ```
   Bot is running!
   Starting bot...
   ```
3. The Flask keep-alive server will run on port 8080

### Step 6: Test Your Bot

1. Open Telegram and search for your bot by username (e.g., `@my_yt_mp3_bot`)
2. Click **"Start"** or send `/start`
3. The bot should reply: "Hi! Send me a YouTube link and I'll convert it to MP3 for you! 🎵"
4. Send any YouTube URL (e.g., `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
5. Wait for the bot to:
   - Download the video audio
   - Convert it to MP3
   - Send the file back to you

## Usage Instructions

### Basic Commands

- `/start` - Get a welcome message and instructions

### Sending YouTube Links

Just send any YouTube URL in one of these formats:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/watch?v=VIDEO_ID&list=...` (playlist links work too)

The bot will:
1. Validate the URL
2. Download the audio (best quality available)
3. Convert to MP3 at 192kbps
4. Send the MP3 file to you
5. Delete the file from the server (by default)

### File Deletion Behavior

By default, the bot **deletes downloaded MP3 files** after sending them to save disk space on Replit.

To change this behavior:
1. Go to your Replit **Secrets**
2. Add a new secret:
   - **Key**: `DELETE_FILES_AFTER_SEND`
   - **Value**: `false`
3. Restart the bot

**Note**: Keeping files will consume storage space. Replit's free tier has limited storage.

## Monitoring and Logs

### Viewing Logs

Logs are displayed in the Replit console when you run the bot. You'll see:
- Bot startup messages
- Incoming messages and commands
- Download progress
- Errors and exceptions

### Log Levels

Control what gets logged by setting the `LOG_LEVEL` secret:
- `DEBUG` - Very detailed, shows everything
- `INFO` - Normal operation messages (default)
- `WARNING` - Only warnings and errors
- `ERROR` - Only errors
- `CRITICAL` - Only critical failures

### Example Log Output

```
2024-10-25 12:00:00 - __main__ - INFO - Starting bot...
2024-10-25 12:00:05 - telegram.ext.Application - INFO - Application started
2024-10-25 12:01:15 - __main__ - INFO - Deleted file: Never Gonna Give You Up.mp3
```

## Project Structure

```
.
├── main.py              # Main bot logic and handlers
├── config.py            # Environment variable configuration
├── keep_alive.py        # Flask server for Replit keep-alive
├── pyproject.toml       # Python dependencies
├── .replit              # Replit configuration
├── .env.example         # Example environment variables
├── .gitignore           # Git ignore rules
├── generated-icon.png   # Bot icon/logo
└── README.md            # This file
```

## Configuration Reference

All configuration is done via environment variables (Replit Secrets):

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `BOT_TOKEN` | ✅ Yes | - | Your Telegram bot token from @BotFather |
| `OPENAI_API_KEY` | ❌ No | - | OpenAI API key (for future AI features) |
| `DATABASE_PATH` | ❌ No | `bot_data.db` | Path to SQLite database file |
| `FLASK_HOST` | ❌ No | `0.0.0.0` | Flask server host |
| `FLASK_PORT` | ❌ No | `8080` | Flask server port |
| `LOG_LEVEL` | ❌ No | `INFO` | Logging verbosity level |
| `DELETE_FILES_AFTER_SEND` | ❌ No | `true` | Delete MP3 files after sending |
| `DOWNLOAD_DIR` | ❌ No | `downloads` | Directory for temporary downloads |

## Troubleshooting

### Bot doesn't respond

1. **Check your BOT_TOKEN**: Make sure it's correct in Replit Secrets
2. **Check logs**: Look for error messages in the console
3. **Restart the bot**: Click Stop, then Run again

### "BOT_TOKEN is required" error

You forgot to add the `BOT_TOKEN` secret. See Step 3 above.

### Download fails

1. **Check the URL**: Make sure it's a valid YouTube link
2. **Video restrictions**: Some videos can't be downloaded (age-restricted, private, etc.)
3. **Replit limits**: Very large videos might exceed Replit's resources

### Bot stops after a while

Replit free tier may shut down inactive apps. The `keep_alive.py` Flask server helps prevent this, but for 24/7 uptime, consider:
- Using a monitoring service like UptimeRobot to ping your bot every 5 minutes
- Upgrading to Replit's paid tier
- Deploying to a different platform (Heroku, Railway, etc.)

### Storage space issues

If you're keeping downloaded files (`DELETE_FILES_AFTER_SEND=false`), you may run out of space:
1. Set `DELETE_FILES_AFTER_SEND=true` (recommended)
2. Manually delete old files in the Shell:
   ```bash
   rm -rf downloads/*
   ```

## Keyboard Instructions for Beginners

If you're new to using a keyboard for coding and navigation:

### Typing Capital Letters

To type a **capital letter** (like "A"):
1. **Hold down the Shift key** (usually has an ⬆ arrow on it)
2. **While holding Shift, press the letter key** (like "a")
3. **Release both keys**

Example: To type "BOT_TOKEN":
- Hold Shift + press B
- Hold Shift + press O
- Hold Shift + press T
- Press underscore (Shift + minus key)
- Continue...

### Common Keyboard Shortcuts

- **Copy**: Ctrl+C (or Cmd+C on Mac)
- **Paste**: Ctrl+V (or Cmd+V on Mac)
- **Save**: Ctrl+S (or Cmd+S on Mac)
- **Undo**: Ctrl+Z (or Cmd+Z on Mac)

## Advanced: Running Locally

To run this bot on your own computer instead of Replit:

1. **Install Python 3.11+** and **FFmpeg**
2. **Clone this repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
3. **Create a `.env` file** (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```
4. **Edit `.env`** and add your `BOT_TOKEN`
5. **Install dependencies**:
   ```bash
   pip install -e .
   ```
6. **Run the bot**:
   ```bash
   python main.py
   ```

## Dependencies

- **python-telegram-bot** - Telegram Bot API wrapper
- **yt-dlp** - YouTube video/audio downloader
- **Flask** - Web framework for keep-alive server
- **python-dotenv** - Environment variable management
- **httpx** - HTTP client (for API requests)
- **openai** - OpenAI API client (optional, for future features)

FFmpeg is required for audio conversion and is pre-installed on Replit.

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License

This project is open source and available under the MIT License.

## Support

If you encounter issues:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review the logs in your Replit console
3. Make sure all environment variables are set correctly
4. Try restarting the bot

## Future Features

Planned enhancements:
- 🎯 Support for playlists
- 🤖 AI-powered music recommendations (using OpenAI)
- 💾 Database for user preferences
- 📊 Usage statistics
- 🎨 Custom audio quality settings
- 🔐 User authentication and rate limiting

---

Made with ❤️ for music lovers everywhere
