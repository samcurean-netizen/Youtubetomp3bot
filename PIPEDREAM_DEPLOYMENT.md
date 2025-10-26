# Pipedream Deployment Guide

This guide explains how to deploy the Telegram bot to Pipedream using webhooks.

## Overview

The webhook-based architecture works as follows:
1. Telegram sends a POST request to your Pipedream endpoint when a user interacts with the bot
2. Pipedream triggers your workflow with the update data
3. Your Python code processes the request (download YouTube audio, transcribe, etc.)
4. Response is sent back to the user via Telegram Bot API

## Prerequisites

- [Pipedream account](https://pipedream.com) (free tier is sufficient for moderate use)
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Basic understanding of webhooks

## Deployment Methods

### Method 1: Using Pipedream's Web UI (Recommended for beginners)

1. **Create a new workflow in Pipedream:**
   - Go to https://pipedream.com/workflows
   - Click "New Workflow"
   - Select "HTTP / Webhook" as the trigger
   - Choose "HTTP Requests" → "New Requests"

2. **Add Python code step:**
   - Click the "+" button to add a new step
   - Search for "Python" and select "Run Python Code"
   - Copy the entire contents of `pipedream_webhook.py` into the code editor
   - Make sure to update the handler function at the bottom

3. **Configure environment variables:**
   - In your workflow, click on "Settings" (gear icon)
   - Go to "Environment Variables"
   - Add: `BOT_TOKEN` = `your-telegram-bot-token`

4. **Deploy the workflow:**
   - Click "Deploy" in the top right
   - Copy the webhook URL (it looks like: `https://eo123abc.m.pipedream.net`)

5. **Set the webhook URL with Telegram:**
   ```bash
   curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=<YOUR_PIPEDREAM_URL>"
   ```
   
   Or visit this URL in your browser:
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=<YOUR_PIPEDREAM_URL>
   ```

6. **Verify webhook is set:**
   ```bash
   curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
   ```

### Method 2: Using Pipedream CLI (For advanced users)

1. **Install Pipedream CLI:**
   ```bash
   npm install -g @pipedream/cli
   ```

2. **Login to Pipedream:**
   ```bash
   pd login
   ```

3. **Create a new workflow:**
   ```bash
   pd init telegram-bot-webhook
   cd telegram-bot-webhook
   ```

4. **Copy the workflow files:**
   - Copy `pipedream_webhook.py` to your workflow directory

5. **Deploy:**
   ```bash
   pd deploy
   ```

6. **Set environment secrets:**
   ```bash
   pd set env BOT_TOKEN=your-telegram-bot-token
   ```

7. **Set webhook with Telegram** (same as Method 1, step 5)

## Pipedream Workflow Structure

### Simplified Workflow (pipedream_workflow.yaml)

```yaml
name: Telegram Bot Webhook Handler
version: 0.0.1

# Trigger on HTTP requests
trigger:
  type: http
  path: /

# Python code step
steps:
  - name: process_telegram_update
    language: python
    code: |
      # Your Python code from pipedream_webhook.py
    requirements:
      - python-telegram-bot>=20.0
      - yt-dlp
      - faster-whisper>=1.0.0
```

## Configuration

### Environment Variables

Set these in Pipedream's workflow settings:

| Variable | Required | Description |
|----------|----------|-------------|
| `BOT_TOKEN` | Yes | Your Telegram bot token from BotFather |

### Dependencies

The following Python packages are required:
- `python-telegram-bot>=20.0`
- `yt-dlp`
- `faster-whisper>=1.0.0`

These are automatically installed by Pipedream when specified in the workflow.

### FFmpeg

FFmpeg is required for audio processing (MP3 conversion). 

**Option 1: Use Pipedream's Built-in FFmpeg** (if available)
- Pipedream's Python environments may have FFmpeg pre-installed

**Option 2: Use Docker-based Workflow**
- Create a Docker-based Pipedream workflow with FFmpeg installed
- Use the following Dockerfile:

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY pipedream_webhook.py .
```

**Option 3: Use static FFmpeg binary**
- Download a static FFmpeg binary and include it in your workflow
- Update the PATH to include the binary

## Limitations and Considerations

### 1. Execution Time Limits
- Pipedream has execution time limits (typically 30-60 seconds for free tier)
- Long audio transcriptions or large YouTube videos may timeout
- Consider implementing a queuing system for long-running tasks

### 2. Cold Starts
- First request after inactivity may be slower
- faster-whisper model needs to be loaded (~150MB)
- Consider using smaller models (tiny/base) for faster cold starts

### 3. Temporary Storage
- Files are stored in `/tmp` which is cleared between invocations
- Maximum storage: typically 512MB-10GB depending on plan
- All files must be cleaned up after processing

### 4. Database Persistence
- SQLite database won't persist between invocations
- Consider using:
  - Pipedream Data Stores (simple key-value store)
  - External database (PostgreSQL, MongoDB, etc.)
  - For simple cases, you can skip persistence

### 5. Concurrent Requests
- Pipedream handles concurrent requests automatically
- Each request runs in isolation
- Be mindful of rate limits on Telegram API

## Testing

### 1. Test the webhook endpoint
```bash
curl -X POST https://your-pipedream-url.m.pipedream.net \
  -H "Content-Type: application/json" \
  -d '{
    "update_id": 123456789,
    "message": {
      "message_id": 1,
      "from": {"id": 123, "first_name": "Test"},
      "chat": {"id": 123, "type": "private"},
      "text": "/start"
    }
  }'
```

### 2. Test bot commands
- Send `/start` to your bot
- Send a YouTube URL
- Send a voice message
- Check Pipedream logs for any errors

## Monitoring and Debugging

### View Logs
1. Go to your workflow in Pipedream
2. Click on "Logs" tab
3. View real-time execution logs
4. Check for errors and performance metrics

### Common Issues

#### Issue: Webhook not receiving updates
**Solution:**
- Verify webhook is set correctly: `getWebhookInfo`
- Check that URL is accessible (test with curl)
- Ensure no other webhook is set

#### Issue: FFmpeg not found
**Solution:**
- Use Docker-based workflow with FFmpeg
- Or use a static FFmpeg binary
- Check Pipedream documentation for pre-installed packages

#### Issue: Timeout on large files
**Solution:**
- Reduce `preferredquality` in yt-dlp options
- Use smaller Whisper model (tiny instead of base)
- Consider implementing async processing with webhooks

#### Issue: Database data not persisting
**Solution:**
- Use Pipedream Data Stores:
  ```python
  # Store data
  pd.data_store.set("key", "value")
  
  # Retrieve data
  value = pd.data_store.get("key")
  ```

## Cost Considerations

### Pipedream Free Tier
- 100,000 credits per month
- Each workflow execution consumes credits based on:
  - Execution time
  - Memory usage
  - Number of steps

### Typical Usage
- Simple message handling: ~1-2 credits
- YouTube download: ~10-20 credits
- Audio transcription: ~20-50 credits (depending on duration)

For moderate usage (few hundred messages/day), free tier is sufficient.

## Production Recommendations

1. **Error Handling:**
   - Implement comprehensive error handling
   - Return 200 OK even on errors to avoid webhook retries
   - Log errors to external service (Sentry, etc.)

2. **Rate Limiting:**
   - Implement rate limiting per user
   - Use Pipedream Data Stores to track usage

3. **Security:**
   - Validate webhook requests (check Telegram secret token)
   - Sanitize user inputs
   - Implement access controls

4. **Monitoring:**
   - Set up alerts for failures
   - Monitor execution time and credit usage
   - Track error rates

5. **Scaling:**
   - Use Pipedream's paid plans for higher limits
   - Consider queueing for long-running tasks
   - Implement caching for frequently accessed data

## Migration from Polling

If you're migrating from the polling-based version:

1. **Stop the old bot:**
   - Shut down the polling-based bot
   - Remove the webhook if one was set previously

2. **Delete webhook (if any):**
   ```bash
   curl "https://api.telegram.org/bot<TOKEN>/deleteWebhook"
   ```

3. **Deploy new webhook version** (follow deployment steps above)

4. **Test thoroughly:**
   - Verify all commands work
   - Test error scenarios
   - Monitor for issues

## Support and Resources

- [Pipedream Documentation](https://pipedream.com/docs)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [python-telegram-bot Documentation](https://python-telegram-bot.readthedocs.io/)
- [yt-dlp Documentation](https://github.com/yt-dlp/yt-dlp)
- [faster-whisper Documentation](https://github.com/guillaumekln/faster-whisper)

## Example: Setting Up Webhook

```bash
# 1. Get your Pipedream webhook URL
PIPEDREAM_URL="https://eo123abc.m.pipedream.net"

# 2. Get your bot token
BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrsTUVwxyz"

# 3. Set webhook
curl "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook?url=${PIPEDREAM_URL}"

# Expected response:
# {"ok":true,"result":true,"description":"Webhook was set"}

# 4. Verify webhook
curl "https://api.telegram.org/bot${BOT_TOKEN}/getWebhookInfo"

# Expected response should show your URL and pending_update_count: 0
```

## Troubleshooting Checklist

- [ ] Bot token is correct and set in environment variables
- [ ] Webhook URL is correct and accessible
- [ ] Webhook is set with Telegram (check with getWebhookInfo)
- [ ] Python dependencies are installed
- [ ] FFmpeg is available (if using YouTube download)
- [ ] Logs show incoming webhook requests
- [ ] No other bot instance is polling
- [ ] Temporary directory (/tmp) is writable
- [ ] Execution time is within limits

## Next Steps

After successful deployment:
1. Monitor the bot for a few days
2. Implement additional features as needed
3. Set up proper logging and alerting
4. Consider adding analytics
5. Implement user feedback mechanism
