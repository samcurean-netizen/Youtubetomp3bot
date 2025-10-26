# Quick Start: Deploy to Pipedream in 5 Minutes

This guide will get your Telegram bot running on Pipedream in under 5 minutes.

## Prerequisites

- [ ] Telegram bot token from [@BotFather](https://t.me/botfather)
- [ ] [Pipedream account](https://pipedream.com/auth/signup) (free)

## Step 1: Create Pipedream Workflow (2 minutes)

1. **Go to Pipedream:** https://pipedream.com/workflows
2. **Click "New Workflow"**
3. **Select trigger:**
   - Choose "HTTP / Webhook"
   - Select "New Requests"
   - Keep the default settings
4. **Copy your webhook URL** - it looks like: `https://eo123abc.m.pipedream.net`

## Step 2: Add Python Code (2 minutes)

1. **Click the "+" button** below the trigger to add a step
2. **Search for "Python"** and select "Run Python Code"
3. **Replace the default code** with the contents of `pipedream_handler.py`
   - You can open the file and copy all contents
   - Paste into the Pipedream code editor
4. **Add dependencies** - In the "Packages" section, add:
   ```
   python-telegram-bot
   yt-dlp
   faster-whisper
   ```

## Step 3: Configure Environment Variables (30 seconds)

1. **Click the gear icon** (Settings) in the top right
2. **Go to "Environment Variables"**
3. **Add new variable:**
   - Name: `BOT_TOKEN`
   - Value: Your Telegram bot token (from BotFather)
4. **Click "Save"**

## Step 4: Deploy (10 seconds)

1. **Click "Deploy"** in the top right corner
2. **Wait for deployment** to complete (green checkmark)

## Step 5: Set Telegram Webhook (30 seconds)

Run this command in your terminal (replace with your values):

```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=<YOUR_PIPEDREAM_URL>"
```

**Example:**
```bash
curl "https://api.telegram.org/bot123456789:ABCdefGHIjklMNOpqrsTUVwxyz/setWebhook?url=https://eo123abc.m.pipedream.net"
```

You should see:
```json
{"ok":true,"result":true,"description":"Webhook was set"}
```

### Alternative: Use the setup script

```bash
export BOT_TOKEN="your-bot-token"
export WEBHOOK_URL="your-pipedream-url"
./setup_webhook.sh
```

## Step 6: Test Your Bot! (1 minute)

1. **Open Telegram** and find your bot
2. **Send `/start`** - you should get a welcome message
3. **Send a YouTube URL** - bot will download and send MP3
4. **Send a voice message** - bot will transcribe it

## Verify Setup

Check webhook status:
```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
```

Expected output:
```json
{
  "ok": true,
  "result": {
    "url": "https://eo123abc.m.pipedream.net",
    "has_custom_certificate": false,
    "pending_update_count": 0
  }
}
```

## Monitoring

**View logs in Pipedream:**
1. Go to your workflow
2. Click "Logs" tab
3. See real-time execution logs

Each bot interaction will show up as a new event with full logs.

## Common Issues

### Bot not responding?

**Check 1:** Is webhook set?
```bash
curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"
```

**Check 2:** Is Pipedream workflow deployed?
- Look for green checkmark in Pipedream UI

**Check 3:** Is BOT_TOKEN correct?
- Go to workflow Settings → Environment Variables
- Verify the token matches your bot

**Check 4:** Check logs
- Go to Logs tab in Pipedream
- Look for errors

### FFmpeg not found?

This is expected if Pipedream's Python environment doesn't include FFmpeg. 

**Solutions:**
1. Use Pipedream's Docker-based workflows with FFmpeg
2. Wait for Pipedream to add FFmpeg to their environment
3. Use a static FFmpeg binary (advanced)

For now, **transcription will work** but YouTube downloads may fail without FFmpeg.

### Timeout errors?

Large files may timeout on free tier (30-60 second limit).

**Solutions:**
1. Upgrade to Pipedream paid plan (longer timeouts)
2. Use smaller Whisper model (`tiny` instead of `base`)
3. Implement async processing with separate workflows

## Next Steps

- ✅ Read the [Full Deployment Guide](PIPEDREAM_DEPLOYMENT.md) for advanced configuration
- ✅ Customize the bot code for your needs
- ✅ Add more features (see `main.py` for inspiration)
- ✅ Set up monitoring and alerts
- ✅ Share your bot with friends!

## Need Help?

- Check [PIPEDREAM_DEPLOYMENT.md](PIPEDREAM_DEPLOYMENT.md) for detailed troubleshooting
- Review Pipedream logs for error messages
- Verify all steps above are completed

## Cost

**Free tier includes:**
- 100,000 credits/month
- Enough for hundreds of bot interactions daily
- No credit card required

Typical usage:
- Simple message: ~1 credit
- YouTube download: ~10-20 credits
- Transcription: ~20-50 credits

**Your bot should run comfortably on the free tier! 🎉**
