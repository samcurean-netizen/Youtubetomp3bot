# Architecture Overview

This document explains the architecture of both deployment modes.

## Polling Mode Architecture

```
┌─────────────────┐
│  Telegram User  │
└────────┬────────┘
         │ Sends message
         ▼
┌─────────────────────────┐
│   Telegram Servers      │
│                         │
│  - Stores messages      │
│  - Provides Bot API     │
└────────┬────────────────┘
         │ Bot polls for updates (getUpdates)
         ▼
┌─────────────────────────────────────────┐
│         Your Server (VPS/Replit)        │
│  ┌───────────────────────────────────┐  │
│  │        main.py (Bot Process)      │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │  Application.run_polling()  │  │  │
│  │  └─────────────────────────────┘  │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │  Command Handlers           │  │  │
│  │  │  - /start                   │  │  │
│  │  │  - YouTube downloads        │  │  │
│  │  │  - Audio transcription      │  │  │
│  │  └─────────────────────────────┘  │  │
│  └───────────────┬───────────────────┘  │
│                  │                       │
│  ┌───────────────▼───────────────────┐  │
│  │      database.py (SQLite)         │  │
│  │  - Chat settings                  │  │
│  │  - Processed messages             │  │
│  │  - Audio file IDs                 │  │
│  └───────────────────────────────────┘  │
│                                          │
│  ┌───────────────────────────────────┐  │
│  │    transcription.py               │  │
│  │  - faster-whisper model           │  │
│  │  - Audio file processing          │  │
│  └───────────────────────────────────┘  │
│                                          │
│  ┌───────────────────────────────────┐  │
│  │   Flask Keep-Alive (Port 8080)    │  │
│  │  - Health check endpoint          │  │
│  │  - Prevents sleep on free tiers   │  │
│  └───────────────────────────────────┘  │
└──────────────────────────────────────────┘
         │ Bot sends responses
         ▼
┌─────────────────────────┐
│   Telegram Servers      │
│  - Delivers messages    │
└────────┬────────────────┘
         │ User receives
         ▼
┌─────────────────┐
│  Telegram User  │
└─────────────────┘
```

### Polling Mode Flow

1. User sends message to bot
2. Telegram stores the message
3. Bot polls Telegram servers every 1-2 seconds
4. Bot receives update and processes it
5. Bot calls appropriate handler
6. Handler processes request (download, transcribe, etc.)
7. Bot sends response back to user via Telegram API

### Polling Mode Components

- **main.py**: Entry point, bot initialization, handlers
- **database.py**: SQLite operations, settings storage
- **transcription.py**: Audio transcription with faster-whisper
- **Flask server**: Keep-alive HTTP server on port 8080

---

## Webhook Mode Architecture

```
┌─────────────────┐
│  Telegram User  │
└────────┬────────┘
         │ Sends message
         ▼
┌─────────────────────────────────────────┐
│         Telegram Servers                │
│                                         │
│  - Stores messages                      │
│  - Immediately sends to webhook URL     │
└────────┬────────────────────────────────┘
         │ HTTP POST with update
         ▼
┌─────────────────────────────────────────┐
│     Pipedream (Serverless Platform)     │
│  ┌───────────────────────────────────┐  │
│  │     HTTP Trigger (Step 1)         │  │
│  │  - Receives webhook POST          │  │
│  │  - Parses JSON body               │  │
│  └───────────────┬───────────────────┘  │
│                  │                       │
│  ┌───────────────▼───────────────────┐  │
│  │  Python Code Step (Step 2)        │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │  pipedream_handler.py       │  │  │
│  │  │                             │  │  │
│  │  │  - TelegramWebhookHandler   │  │  │
│  │  │  - Process update           │  │  │
│  │  │  - Route to handlers        │  │  │
│  │  │  - YouTube download         │  │  │
│  │  │  - Audio transcription      │  │  │
│  │  └─────────────────────────────┘  │  │
│  │                                   │  │
│  │  Dependencies (auto-installed):  │  │
│  │  - python-telegram-bot           │  │
│  │  - yt-dlp                        │  │
│  │  - faster-whisper                │  │
│  └───────────────┬───────────────────┘  │
│                  │                       │
│  ┌───────────────▼───────────────────┐  │
│  │  Temporary Storage (/tmp)         │  │
│  │  - Downloaded files               │  │
│  │  - Converted audio                │  │
│  │  - Cleaned up after processing    │  │
│  └───────────────────────────────────┘  │
│                                          │
│  ┌───────────────────────────────────┐  │
│  │  Environment Variables            │  │
│  │  - BOT_TOKEN                      │  │
│  └───────────────────────────────────┘  │
└──────────────────┬───────────────────────┘
                   │ Returns HTTP 200 OK
                   │
         ┌─────────┴─────────┐
         │                   │
         ▼                   ▼
    [Success]           [Telegram]
  (Pipedream logs)    (Gets 200, stops)
         │                   
         │ Bot sends response via Telegram API
         ▼
┌─────────────────────────┐
│   Telegram Servers      │
│  - Delivers messages    │
└────────┬────────────────┘
         │ User receives
         ▼
┌─────────────────┐
│  Telegram User  │
└─────────────────┘
```

### Webhook Mode Flow

1. User sends message to bot
2. Telegram immediately sends HTTP POST to webhook URL
3. Pipedream receives the request and triggers workflow
4. Python code processes the update
5. Handler downloads/transcribes/responds
6. Bot sends response via Telegram Bot API
7. Returns HTTP 200 to Telegram
8. User receives the response

### Webhook Mode Components

- **HTTP Trigger**: Receives POST requests from Telegram
- **pipedream_handler.py**: Main handler, routing, processing
- **TelegramWebhookHandler**: Class handling all bot logic
- **Temporary storage**: `/tmp` for file operations
- **Environment variables**: BOT_TOKEN stored securely

---

## Component Details

### Shared Components

Both modes use the same core functionality:

#### 1. YouTube Download Flow

```
User sends URL
    ↓
Validate URL (youtube.com or youtu.be)
    ↓
yt-dlp downloads best audio
    ↓
FFmpeg converts to MP3
    ↓
Upload MP3 to Telegram
    ↓
Delete temporary files
    ↓
Send success message
```

#### 2. Audio Transcription Flow

```
User sends voice/audio
    ↓
Download file to temp location
    ↓
Load faster-whisper model
    ↓
Transcribe audio
    ↓
Extract text and language
    ↓
Send transcription to user
    ↓
Delete temporary files
```

#### 3. Command Handling

```
Message received
    ↓
Parse message type
    ↓
Route to handler:
    - /start → Welcome message
    - YouTube URL → Download handler
    - Audio file → Transcription handler
    - "change" → Settings handler
    - Other text → Error message
```

---

## Data Flow

### Polling Mode Data Flow

```
Telegram → [Poll] → Bot Process → Handler → External API/Processing
                         ↓              ↓
                    Database      File System
                         ↓              ↓
                    SQLite         /downloads/
                         ↓              ↓
                   (Persistent)   (Persistent)
```

### Webhook Mode Data Flow

```
Telegram → [POST] → Pipedream → Handler → External API/Processing
                         ↓           ↓
                    Env Vars    /tmp/
                         ↓           ↓
                   (Persistent) (Ephemeral)
```

---

## Scalability

### Polling Mode Scaling

```
[Bot Instance 1] → Telegram
[Bot Instance 2] → Telegram  (requires coordination)
[Bot Instance 3] → Telegram  (not recommended)
```

**Note:** Multiple polling instances can conflict. Not recommended.

### Webhook Mode Scaling

```
Telegram → Load Balancer → [Function Instance 1]
                        → [Function Instance 2]
                        → [Function Instance 3]
                        → [Function Instance N]
```

**Note:** Automatic horizontal scaling. Platform handles it.

---

## Security Considerations

### Polling Mode

- ✅ Bot token stored in environment variables
- ✅ No public endpoint needed
- ✅ Can run behind firewall
- ⚠️ Must secure the server
- ⚠️ Keep dependencies updated

### Webhook Mode

- ✅ Bot token stored in platform secrets
- ✅ HTTPS enforced automatically
- ✅ Platform handles security patches
- ⚠️ Public endpoint (but authenticated by Telegram)
- ⚠️ Validate webhook requests (optional: use secret token)

---

## Monitoring

### Polling Mode Monitoring

```
Application Logs → File/Console
     ↓
[Monitor manually or use logging service]
     ↓
Alerts/Dashboards
```

### Webhook Mode Monitoring

```
Function Execution → Platform Logs (Pipedream)
     ↓
Built-in Dashboard
     ↓
Real-time monitoring, alerts, metrics
```

---

## File Operations

### Polling Mode

```
Download → /app/downloads/video.mp3
Process  → /app/downloads/video.mp3
Upload   → Telegram
Clean    → rm /app/downloads/video.mp3
```

Files persist until explicitly deleted.

### Webhook Mode

```
Download → /tmp/telegram_bot/video.mp3
Process  → /tmp/telegram_bot/video.mp3
Upload   → Telegram
Clean    → rm /tmp/telegram_bot/video.mp3
```

Files automatically cleared between invocations.

---

## Error Handling

### Polling Mode

```
Error occurs
    ↓
Log error
    ↓
Send error message to user
    ↓
Continue polling (bot stays running)
```

### Webhook Mode

```
Error occurs
    ↓
Log error (Pipedream logs)
    ↓
Send error message to user
    ↓
Return HTTP 200 (prevent Telegram retry)
    ↓
Function terminates
```

---

## Cost Structure

### Polling Mode

```
Fixed Costs:
- Server: $5-20/month (always running)
- Bandwidth: Usually included
- Storage: Usually included

Total: $5-20/month (predictable)
```

### Webhook Mode

```
Variable Costs:
- Requests: Free tier → 100k/month
- Compute: Charged per execution time
- Storage: Temporary (free)

Total: $0-19/month (scales with usage)
```

---

## Deployment Process

### Polling Mode

```
1. Set up server
2. Install dependencies
3. Set environment variables
4. Run: python main.py
5. Keep process running (systemd/screen)
```

### Webhook Mode

```
1. Create Pipedream workflow
2. Copy handler code
3. Set environment variables
4. Deploy workflow
5. Set webhook URL with Telegram
```

---

## Maintenance

### Polling Mode Maintenance

- Update dependencies manually
- Monitor server health
- Restart on crashes
- Manage disk space
- Apply security patches

### Webhook Mode Maintenance

- Platform handles most updates
- Monitor execution logs
- Update code when needed
- Minimal ongoing maintenance

---

## Summary

**Polling Mode:**
- Traditional, proven architecture
- Full control
- Predictable costs
- More maintenance

**Webhook Mode:**
- Modern, serverless architecture
- Automatic scaling
- Pay-per-use
- Less maintenance

Both architectures provide the same functionality to users, just with different operational characteristics.
