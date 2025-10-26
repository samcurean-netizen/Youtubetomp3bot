# Complete Pipedream Deployment Guide for Telegram Bot

This comprehensive guide walks you through deploying your Telegram bot to Pipedream using webhooks, step by step. No prior Pipedream knowledge required!

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Step 1: Pipedream Account Setup](#step-1-pipedream-account-setup)
4. [Step 2: Get Your Telegram Bot Token](#step-2-get-your-telegram-bot-token)
5. [Step 3: Create a Pipedream Workflow](#step-3-create-a-pipedream-workflow)
6. [Step 4: Add Python Code](#step-4-add-python-code)
7. [Step 5: Configure Environment Variables](#step-5-configure-environment-variables)
8. [Step 6: Deploy the Workflow](#step-6-deploy-the-workflow)
9. [Step 7: Get Your Webhook URL](#step-7-get-your-webhook-url)
10. [Step 8: Register Webhook with Telegram](#step-8-register-webhook-with-telegram)
11. [Step 9: Test Your Bot](#step-9-test-your-bot)
12. [Monitoring and Logs](#monitoring-and-logs)
13. [Troubleshooting](#troubleshooting)
14. [Maintenance](#maintenance)
15. [Cost Considerations](#cost-considerations)
16. [Advanced Configuration](#advanced-configuration)

---

## Overview

### How Webhooks Work

The webhook-based architecture works as follows:
1. **User sends message** → Telegram Bot receives it
2. **Telegram sends update** → POST request to your Pipedream webhook URL
3. **Pipedream triggers** → Executes your Python code with the update data
4. **Your code processes** → Downloads YouTube audio, transcribes, etc.
5. **Bot responds** → Sends result back to user via Telegram Bot API

### Why Use Pipedream?

- ✅ **Free tier** with generous limits (100,000 credits/month)
- ✅ **Serverless** - No server maintenance required
- ✅ **Auto-scaling** - Handles traffic spikes automatically
- ✅ **Pay per use** - Only charged for actual usage
- ✅ **Easy deployment** - Deploy in minutes via web UI
- ✅ **Built-in logging** - Real-time execution logs and debugging

---

## Prerequisites

Before you begin, make sure you have:

### 1. Pipedream Account (Free)

**What you need:** A free Pipedream account

**How to get it:**
1. Go to [https://pipedream.com/auth/signup](https://pipedream.com/auth/signup)
2. Sign up using one of these methods:
   - GitHub account (recommended)
   - Google account
   - Email and password
3. Verify your email if required
4. No credit card needed for free tier!

### 2. Telegram Bot Token

**What you need:** A bot token from Telegram's BotFather

**How to get it:** See [Step 2](#step-2-get-your-telegram-bot-token) below

### 3. Required Knowledge

- ✅ Basic understanding of how Telegram bots work
- ✅ Ability to copy/paste text and follow instructions
- ✅ Access to a terminal/command line (for webhook setup)
- ❌ No programming knowledge required!

---

## Step 1: Pipedream Account Setup

### 1.1 Create Your Account

1. **Visit Pipedream:**
   - Open your browser and go to [https://pipedream.com/auth/signup](https://pipedream.com/auth/signup)

2. **Choose sign-up method:**
   - Click **"Continue with GitHub"** (recommended) OR
   - Click **"Continue with Google"** OR
   - Enter your email and create a password

3. **Complete registration:**
   - Follow the prompts to verify your email
   - Accept the terms of service
   - You'll be redirected to the Pipedream dashboard

### 1.2 Familiarize with Dashboard

After logging in, you'll see:
- **Left sidebar:** Navigation menu
- **Workflows:** Where you'll create your bot workflow
- **Sources:** Webhook triggers and data sources
- **Connected Accounts:** Third-party integrations
- **Settings:** Account preferences

---

## Step 2: Get Your Telegram Bot Token

If you already have a bot token, skip to [Step 3](#step-3-create-a-pipedream-workflow).

### 2.1 Open BotFather on Telegram

1. **Open Telegram** (mobile app or desktop)
2. **Search for:** `@BotFather`
3. **Start a chat** with BotFather (it's the official Telegram bot for managing bots)

### 2.2 Create a New Bot

1. **Send command:** `/newbot`
2. **Choose a name:** BotFather will ask for a name (e.g., "My Audio Bot")
   - This is the display name users will see
3. **Choose a username:** Must end in `bot` (e.g., `my_audio_bot` or `MyAudioBot`)
   - This must be unique across all Telegram
   - Example: `john_audio_bot`

### 2.3 Save Your Bot Token

After creating the bot, BotFather will send you a message like:

```
Done! Congratulations on your new bot.
You will find it at t.me/your_bot_name

Use this token to access the HTTP API:
123456789:ABCdefGHIjklMNOpqrsTUVwxyz-1234567890

Keep your token secure and store it safely...
```

**IMPORTANT:** 
- ✅ Copy this token immediately
- ✅ Store it somewhere safe (you'll need it in Step 5)
- ❌ Never share this token publicly
- ❌ Don't commit it to GitHub or public repositories

### 2.4 Optional: Customize Your Bot

You can optionally customize your bot with BotFather:
- `/setdescription` - Set bot description
- `/setabouttext` - Set about text
- `/setuserpic` - Set profile picture
- `/setcommands` - Set command list (e.g., `start - Start the bot`)

---

## Step 3: Create a Pipedream Workflow

Now let's create the workflow that will handle your bot's webhooks.

### 3.1 Navigate to Workflows

1. **Log in to Pipedream:** [https://pipedream.com](https://pipedream.com)
2. **Click "Workflows"** in the left sidebar
   - If you're new, you might see a welcome screen - click "Create Workflow"
   - If you have existing workflows, click the **"New Workflow"** button (top right)

### 3.2 Create New Workflow

You'll see a workflow builder with these sections:
- **Trigger:** How the workflow starts (we'll use HTTP/Webhook)
- **Steps:** Actions that happen when triggered
- **Test:** Test the workflow with sample data

### 3.3 Configure the HTTP Trigger

1. **Trigger section** (top of the page):
   - You'll see "Select a trigger" or an HTTP trigger by default
   
2. **If you need to select a trigger:**
   - Click on the trigger area
   - In the search box, type: `HTTP`
   - Select **"HTTP / Webhook"**
   - Choose **"HTTP API"** or **"New Requests"**

3. **Configure trigger settings:**
   - **HTTP Method:** Leave as `POST` (Telegram sends POST requests)
   - **Path:** Leave as `/` (default)
   - **Authentication:** Leave as `None` (Telegram uses your bot token internally)
   
4. **Save trigger:**
   - The trigger is saved automatically
   - You'll see a webhook URL appear (we'll copy this in Step 7)

### 3.4 Name Your Workflow

1. **Click on the workflow title** (top left, usually says "Untitled Workflow")
2. **Rename it** to something descriptive:
   - Example: `Telegram Audio Bot Webhook`
   - Example: `My Bot Handler`
3. The name is saved automatically

---

## Step 4: Add Python Code

Now we'll add the Python code that processes Telegram updates.

### 4.1 Which Code File to Use?

This repository contains two files for Pipedream:
- **`pipedream_handler.py`** ✅ **RECOMMENDED** - Complete, well-structured handler
- **`pipedream_webhook.py`** - Alternative implementation

**Use `pipedream_handler.py` for this guide.**

### 4.2 Open the Code File

1. **In this repository**, open the file `pipedream_handler.py`
2. You can:
   - View it on GitHub
   - Open it in your local code editor
   - View it in the terminal: `cat pipedream_handler.py`

### 4.3 Add Python Code Step in Pipedream

1. **In your Pipedream workflow**, below the HTTP trigger:
   - Click the **large "+" button** (Add Step)
   
2. **Search for Python:**
   - In the search box, type: `python`
   - Select **"Python"** (with the Python logo)
   - Choose **"Run Python code"** or **"Python Code"**

3. **You'll see a code editor** with some default code

### 4.4 Copy the Handler Code

1. **Select ALL code** in `pipedream_handler.py`:
   - Open the file in your editor
   - Select all (Ctrl+A / Cmd+A)
   - Copy (Ctrl+C / Cmd+C)

2. **Back in Pipedream:**
   - **Delete** all the default code in the editor
   - **Paste** the contents of `pipedream_handler.py`
   - The code should be ~426 lines

3. **Verify the code:**
   - Scroll to the bottom
   - You should see a `def handler(pd: "pipedream"):` function
   - This is the main entry point

### 4.5 Add Python Dependencies

The code needs these Python packages to run.

1. **Look for the "Packages" or "Add package" button:**
   - Usually below the code editor
   - Might be labeled "Packages", "Dependencies", or "Add pip packages"

2. **Add each package** (click "Add package" for each):
   - `python-telegram-bot` (or `python-telegram-bot>=20.0`)
   - `yt-dlp`
   - `faster-whisper` (or `faster-whisper>=1.0.0`)

3. **Pipedream will install these** when you deploy

**Note:** If you don't see a packages section, Pipedream might auto-detect imports. You can proceed and add them later if needed.

### 4.6 Optional: Rename the Step

1. **Click on the step name** (usually says "python")
2. **Rename** to something descriptive: `process_telegram_update`
3. This makes logs easier to read

---

## Step 5: Configure Environment Variables

Your bot token needs to be stored securely as an environment variable.

### 5.1 Open Workflow Settings

1. **Look for the settings icon** (gear/cog icon):
   - Usually in the **top-right corner** of the workflow
   - OR click on your workflow name dropdown menu
   
2. **Click "Settings"** or the gear icon

### 5.2 Navigate to Environment Variables

1. **In the settings panel**, look for:
   - **"Environment Variables"**
   - OR **"Secrets"**
   - OR **"Environment"** tab

2. **Click on it** to open the environment variables section

### 5.3 Add BOT_TOKEN Variable

1. **Click "Add Environment Variable"** or similar button

2. **Fill in the fields:**
   - **Name/Key:** `BOT_TOKEN` (exactly like this, all caps)
   - **Value:** Paste your bot token from Step 2
     - Example: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz-1234567890`
   - **Type:** Select "Secret" or "Encrypted" if available (keeps it hidden in logs)

3. **Save** the environment variable

### 5.4 Verify Configuration

1. **Check that the variable appears** in the list as `BOT_TOKEN`
2. **The value should be hidden** (shown as `•••••••` or similar)
3. **Close the settings panel**

**Important:** The variable name MUST be exactly `BOT_TOKEN` (all uppercase) - the code looks for this exact name.

---

## Step 6: Deploy the Workflow

### 6.1 Deploy

1. **Look for the "Deploy" button:**
   - Usually in the **top-right corner**
   - Might be green or blue
   - Next to "Save" or "Test"

2. **Click "Deploy"**:
   - Pipedream will validate your code
   - Install Python dependencies (this may take 30-60 seconds)
   - Activate the workflow

3. **Wait for deployment:**
   - You'll see a progress indicator
   - Status will change to "Deployed" or show a ✅ checkmark
   - If there are errors, see [Troubleshooting](#troubleshooting)

### 6.2 Confirm Deployment

After deployment, you should see:
- ✅ **Green checkmark** or "Deployed" status
- ✅ **HTTP endpoint is active** (webhook URL is live)
- ✅ **No error messages**

---

## Step 7: Get Your Webhook URL

After deployment, you need to copy the webhook URL to register it with Telegram.

### 7.1 Find the Webhook URL

1. **Look at the HTTP trigger step** (first step in your workflow)
2. **Find the webhook URL** - it will look like:
   ```
   https://eo123abc.m.pipedream.net
   ```
   OR
   ```
   https://eo123abc456def.m.pipedream.net
   ```

3. **Location of URL:**
   - Usually shown prominently in the trigger section
   - Might be labeled: "Endpoint URL", "Webhook URL", "HTTP Endpoint"
   - Click a "Copy" icon/button if available

### 7.2 Copy the URL

**Method 1: Click to Copy**
- Click the copy icon next to the URL

**Method 2: Manual Copy**
- Select the entire URL
- Copy it (Ctrl+C / Cmd+C)

### 7.3 Save the URL

**Save this URL somewhere safe** - you'll need it for the next step!

Example: Store it in a text file or notes app temporarily.

---

## Step 8: Register Webhook with Telegram

Now you need to tell Telegram to send updates to your Pipedream webhook URL.

### 8.1 Prepare Your Information

You need two things:
1. **Your bot token** (from Step 2)
2. **Your Pipedream webhook URL** (from Step 7)

### 8.2 Choose Registration Method

You can register the webhook using either:
- **Method A:** Browser (easiest)
- **Method B:** Terminal/Command Line (recommended)
- **Method C:** Setup Script (quickest)

### Method A: Using Browser (Easiest)

1. **Open your web browser**

2. **Create the URL:**
   Replace `<BOT_TOKEN>` and `<WEBHOOK_URL>` with your actual values:
   ```
   https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=<WEBHOOK_URL>
   ```

3. **Example:**
   ```
   https://api.telegram.org/bot123456789:ABCdefGHI/setWebhook?url=https://eo123abc.m.pipedream.net
   ```

4. **Paste in browser** and press Enter

5. **Expected response:**
   ```json
   {"ok":true,"result":true,"description":"Webhook was set"}
   ```

### Method B: Using Terminal/Command Line (Recommended)

1. **Open your terminal** (Command Prompt, PowerShell, Terminal, etc.)

2. **Run this command:**
   ```bash
   curl "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=<WEBHOOK_URL>"
   ```

3. **Replace placeholders** with your actual values:
   ```bash
   curl "https://api.telegram.org/bot123456789:ABCdefGHI/setWebhook?url=https://eo123abc.m.pipedream.net"
   ```

4. **Press Enter**

5. **Expected response:**
   ```json
   {"ok":true,"result":true,"description":"Webhook was set"}
   ```

### Method C: Using Setup Script (Quickest)

This repository includes a helper script.

1. **Open terminal** in the project directory

2. **Run the script:**
   ```bash
   chmod +x setup_webhook.sh
   ./setup_webhook.sh
   ```

3. **Enter your bot token** when prompted

4. **Enter your webhook URL** when prompted

5. **Script will:**
   - Set the webhook
   - Verify it was set correctly
   - Show webhook information

### 8.3 Verify Webhook Registration

After setting the webhook, verify it's working:

1. **Check webhook info:**
   ```bash
   curl "https://api.telegram.org/bot<BOT_TOKEN>/getWebhookInfo"
   ```

2. **Expected response:**
   ```json
   {
     "ok": true,
     "result": {
       "url": "https://eo123abc.m.pipedream.net",
       "has_custom_certificate": false,
       "pending_update_count": 0,
       "max_connections": 40
     }
   }
   ```

3. **Important fields:**
   - `"url"` - Should match your Pipedream URL
   - `"pending_update_count"` - Should be 0 (no queued messages)
   - If `pending_update_count` is high, it means Telegram couldn't deliver updates

### 8.4 Alternative: Use Postman or API Client

If you prefer GUI tools:

1. Open Postman, Insomnia, or any REST client
2. Create a GET request to:
   ```
   https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=<WEBHOOK_URL>
   ```
3. Send the request
4. Check for success response

---

## Step 9: Test Your Bot

Now let's test that everything works!

### 9.1 Open Your Bot on Telegram

1. **Open Telegram** (mobile or desktop)
2. **Search for your bot** using the username you created
   - Example: `@my_audio_bot`
3. **Start a chat** with your bot
   - Click "Start" or send `/start`

### 9.2 Test Commands

#### Test 1: /start Command

1. **Send:** `/start`
2. **Expected response:**
   ```
   Hi! I can help you with:
   🎵 Send me a YouTube link and I'll convert it to MP3
   🎤 Send me a voice message or audio file and I'll transcribe it
   
   All transcription happens locally - no external APIs needed!
   ```

3. **If it works:** ✅ Your bot is responding!
4. **If no response:** See [Troubleshooting](#bot-not-responding)

#### Test 2: YouTube Download

1. **Find a YouTube video** (short video recommended for testing)
   - Example: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`

2. **Send the URL** to your bot

3. **Expected behavior:**
   - Bot sends: "⏳ Downloading..."
   - Then: "📤 Uploading MP3..."
   - Finally: Bot sends the MP3 file

4. **Note:** This requires FFmpeg (see [FFmpeg Availability](#ffmpeg-availability))

#### Test 3: Audio Transcription

1. **Send a voice message** to your bot:
   - Record using Telegram's voice message feature
   - Say something clear in English (or any language)

2. **Expected behavior:**
   - Bot sends: "⏳ Transcribing audio..."
   - Then: "📝 Transcription (en): [your text]"

3. **If transcription fails:** The Whisper model may need to download on first use (~150MB)

### 9.3 Check Pipedream Logs

To see what's happening behind the scenes:

1. **Go to your Pipedream workflow**
2. **Click "Logs" tab** (top of page)
3. **You should see events** for each message you sent
4. **Click on an event** to see:
   - Incoming webhook payload (from Telegram)
   - Python code execution logs
   - Any errors or warnings

### 9.4 Troubleshooting Failed Tests

If tests fail, see the [Troubleshooting](#troubleshooting) section below.

---

## Monitoring and Logs

### 10.1 Viewing Execution Logs

**To view logs:**
1. Go to your workflow in Pipedream
2. Click **"Logs"** or **"Events"** tab
3. You'll see a list of all webhook executions

**Each log entry shows:**
- Timestamp
- Execution duration
- Status (success/error)
- Credits consumed
- Input/output data

### 10.2 Inspecting Individual Events

**Click on an event** to see:
1. **Trigger data:** The incoming webhook from Telegram
2. **Step results:** Output from each step
3. **Logs:** Console logs from your Python code
4. **Errors:** Stack traces if something failed

### 10.3 Real-Time Log Streaming

**Enable real-time logs:**
1. Keep the Logs tab open
2. New events appear automatically
3. Useful for debugging live issues

### 10.4 Log Retention

- **Free tier:** Logs retained for 3 days
- **Paid tiers:** Longer retention periods
- Export important logs if needed

### 10.5 Using Logger in Code

The code uses Python's `logging` module:
```python
logger.info("This appears in Pipedream logs")
logger.error("Errors are highlighted")
```

All `logger` statements appear in Pipedream's log viewer.

---

## Troubleshooting

### Issue 1: Bot Not Responding

**Symptoms:**
- Sending `/start` has no response
- Bot appears offline

**Solutions:**

1. **Check webhook is set:**
   ```bash
   curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"
   ```
   - Verify `url` matches your Pipedream URL
   - Check `pending_update_count` (should be 0)

2. **Check workflow is deployed:**
   - Go to Pipedream workflow
   - Look for "Deployed" status with ✅
   - If not deployed, click "Deploy"

3. **Check BOT_TOKEN:**
   - Go to workflow Settings → Environment Variables
   - Verify `BOT_TOKEN` is set correctly
   - No extra spaces or quotes
   - If wrong, update and redeploy

4. **Check Pipedream logs:**
   - Go to Logs tab
   - Send a message to bot
   - Do you see a new event?
   - If yes: Check for errors in logs
   - If no: Webhook might not be registered correctly

5. **Remove old webhooks:**
   ```bash
   curl "https://api.telegram.org/bot<TOKEN>/deleteWebhook"
   ```
   Then re-register (Step 8)

### Issue 2: FFmpeg Not Found

**Symptoms:**
- YouTube download fails with "FFmpeg not found" error
- Error message mentions `ffmpeg` or `avconv`

**Background:**
Pipedream's Python environment may not include FFmpeg by default.

**Solutions:**

**Option A: Use Docker-Based Workflow** (Advanced)
1. Create a Docker-based Pipedream workflow
2. Use this Dockerfile:
   ```dockerfile
   FROM python:3.11-slim
   
   RUN apt-get update && apt-get install -y \
       ffmpeg \
       && rm -rf /var/lib/apt/lists/*
   
   RUN pip install python-telegram-bot yt-dlp faster-whisper
   ```

**Option B: Use Static FFmpeg Binary** (Advanced)
1. Download static FFmpeg binary for Linux
2. Upload to Pipedream or external storage
3. Modify code to use the binary path

**Option C: Wait and Use Transcription Only**
- Transcription works without FFmpeg
- YouTube downloads require FFmpeg
- You can still use the bot for transcription!

**Option D: Request FFmpeg from Pipedream**
- Contact Pipedream support
- Request FFmpeg in Python environments
- They may add it in future updates

**Temporary Workaround:**
Comment out YouTube download functionality:
```python
# In the code, find:
elif 'youtube.com' in text or 'youtu.be' in text:
    await self._download_youtube_audio(update, text)

# Change to:
elif 'youtube.com' in text or 'youtu.be' in text:
    await self.bot.send_message(
        chat_id=chat_id,
        text="⚠️ YouTube downloads temporarily unavailable (FFmpeg required)"
    )
```

### Issue 3: Timeout Errors

**Symptoms:**
- Large files fail to process
- Error: "Execution time limit exceeded"
- Workflow stops mid-processing

**Causes:**
- Free tier has 30-60 second execution limits
- Large videos take too long to download
- Large audio files take too long to transcribe

**Solutions:**

1. **Use shorter videos:**
   - Test with videos under 5 minutes
   - Longer videos may timeout

2. **Use smaller Whisper model:**
   In the code, find:
   ```python
   WhisperModel("base", device="cpu", compute_type="int8")
   ```
   Change to:
   ```python
   WhisperModel("tiny", device="cpu", compute_type="int8")
   ```
   This is faster but less accurate.

3. **Lower audio quality:**
   In the code, find:
   ```python
   'preferredquality': '192',
   ```
   Change to:
   ```python
   'preferredquality': '128',
   ```
   Smaller files = faster processing.

4. **Upgrade Pipedream plan:**
   - Paid plans have longer execution time limits
   - Up to 5 minutes or more

5. **Use async processing:**
   - Advanced: Split into multiple workflows
   - One to download, another to process
   - Use Pipedream Data Stores to pass data

### Issue 4: Whisper Model Download Fails

**Symptoms:**
- First transcription attempt fails
- Error about downloading model
- "Connection timeout" or "Download failed"

**Cause:**
faster-whisper downloads the model on first use (~150MB for base model).

**Solutions:**

1. **Retry after a minute:**
   - Model download may have timed out
   - Try sending another voice message

2. **Check Pipedream disk space:**
   - Models are cached in `/tmp`
   - May be cleared between invocations

3. **Use smaller model:**
   Change to `tiny` model (only ~75MB):
   ```python
   WhisperModel("tiny", device="cpu", compute_type="int8")
   ```

4. **Pre-download model (advanced):**
   - Download model in a separate initialization step
   - Keep workflow "warm" with periodic pings

### Issue 5: Database Errors

**Symptoms:**
- Errors mentioning SQLite or database
- "Database is locked" errors

**Cause:**
The database (`bot_data.db`) is designed for polling mode, not webhooks.

**Solution:**
The webhook handler doesn't use the database - these errors shouldn't occur. If they do:

1. **Check the code:**
   - Make sure you're using `pipedream_handler.py` (not `main.py`)
   - `pipedream_handler.py` doesn't import or use `database.py`

2. **Remove database imports:**
   If you see `import database` in your code, remove it.

### Issue 6: Empty Response from Bot

**Symptoms:**
- Bot responds but message is empty
- Bot sends a message but no text

**Solutions:**

1. **Check logs for errors:**
   - Go to Pipedream logs
   - Look for exceptions or error messages

2. **Check API rate limits:**
   - Telegram has rate limits
   - Wait a minute and try again

3. **Verify message format:**
   - Check if response is being formatted correctly
   - Look for empty strings in code logic

### Issue 7: Webhook Verification Failed

**Symptoms:**
- `setWebhook` returns error
- "URL is invalid" or "URL unreachable"

**Solutions:**

1. **Check URL format:**
   - Must start with `https://` (not `http://`)
   - Pipedream URLs are always HTTPS

2. **Test webhook URL:**
   ```bash
   curl -X POST https://your-webhook-url.m.pipedream.net \
     -H "Content-Type: application/json" \
     -d '{"test": "data"}'
   ```
   Should return 200 status

3. **Ensure workflow is deployed:**
   - Undeployed workflows won't respond
   - Click "Deploy" and wait for confirmation

4. **Check for typos:**
   - Verify you copied the complete URL
   - No extra characters or spaces

### Issue 8: High Credit Usage

**Symptoms:**
- Running out of Pipedream credits quickly
- Usage seems higher than expected

**Solutions:**

1. **Check execution times:**
   - Go to workflow logs
   - Look at duration for each execution
   - Longer executions = more credits

2. **Optimize code:**
   - Use smaller Whisper model (tiny vs base)
   - Lower video quality settings
   - Add caching where possible

3. **Limit usage:**
   - Implement rate limiting per user
   - Use Pipedream Data Stores to track usage

4. **Monitor logs:**
   - Check for infinite loops
   - Look for repeated failed attempts
   - Fix errors to avoid wasted executions

### Issue 9: Slow Response Times

**Symptoms:**
- Bot takes a long time to respond
- Users experience delays

**Causes:**
- Cold starts (first execution after idle period)
- Model loading (Whisper model initialization)
- Large file downloads

**Solutions:**

1. **Cold start mitigation:**
   - Paid plans have faster cold starts
   - Keep workflow "warm" with periodic pings
   - Accept that first use is slower

2. **Optimize model loading:**
   - Use tiny model for faster initialization
   - Model is cached after first load

3. **Set user expectations:**
   - Update status messages: "This may take a minute..."
   - Send progress updates during processing

### Issue 10: "Handler function not found" Error

**Symptoms:**
- Workflow fails with handler error
- Python step doesn't execute

**Cause:**
Pipedream can't find the entry point function.

**Solution:**

1. **Check function name:**
   Make sure your code has:
   ```python
   async def handler(pd: "pipedream"):
       # ... code ...
   ```
   OR
   ```python
   def handler(pd: "pipedream"):
       # ... code ...
   ```

2. **Check indentation:**
   - The handler function should NOT be indented
   - It should be at the module level (no tabs/spaces before `def`)

3. **Re-paste code:**
   - Delete all code in Pipedream
   - Re-paste from `pipedream_handler.py`
   - Ensure no formatting issues

### General Debugging Tips

1. **Enable detailed logging:**
   ```python
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Add debug prints:**
   ```python
   logger.info(f"Debug: {variable_name}")
   ```

3. **Test webhook manually:**
   ```bash
   curl -X POST https://your-webhook.m.pipedream.net \
     -H "Content-Type: application/json" \
     -d '{"update_id":1,"message":{"message_id":1,"from":{"id":123,"first_name":"Test"},"chat":{"id":123,"type":"private"},"text":"/start"}}'
   ```

4. **Check Telegram API status:**
   - Visit [https://telegram.org/](https://telegram.org/)
   - Check if Telegram is experiencing issues

5. **Simplify to isolate:**
   - Test with just `/start` command first
   - Add features one at a time
   - Identify which feature causes issues

---

## Maintenance

### Updating the Bot

**To update your bot code:**

1. **Make changes** to your local `pipedream_handler.py` file
2. **Copy the updated code**
3. **Go to Pipedream workflow**
4. **Paste the new code** into the Python step
5. **Click "Deploy"**
6. **Test** to ensure changes work

**Tip:** Keep a backup of your working code before making changes.

### Viewing Usage Statistics

**To see your usage:**
1. Go to Pipedream dashboard
2. Click **"Usage"** or **"Billing"**
3. You'll see:
   - Credits used this month
   - Workflow invocations
   - Execution time breakdown

### Managing Invocations

**Check workflow invocations:**
1. Go to your workflow
2. Look at the statistics section
3. See total runs, success rate, average duration

### Handling Errors

**Set up error notifications:**
1. Go to workflow Settings
2. Look for "Notifications" or "Alerts"
3. Configure email notifications for:
   - Workflow errors
   - Quota warnings
   - Deployment failures

### Backup and Version Control

**Recommended practices:**

1. **Save code locally:**
   - Keep `pipedream_handler.py` in version control (Git)
   - Track changes over time

2. **Document changes:**
   - Add comments explaining modifications
   - Keep a changelog

3. **Test before deploying:**
   - Test locally if possible
   - Use a test bot for major changes

### Scaling Up

**If your bot becomes popular:**

1. **Upgrade Pipedream plan:**
   - More credits per month
   - Longer execution times
   - Higher rate limits

2. **Optimize code:**
   - Cache frequently used data
   - Implement efficient algorithms
   - Minimize API calls

3. **Consider external database:**
   - Use PostgreSQL, MongoDB, or similar
   - Store user preferences persistently

4. **Add rate limiting:**
   - Prevent abuse
   - Protect your quota

### Deactivating the Bot

**To stop the bot temporarily:**
1. Go to your workflow
2. Click "Disable" or "Pause"
3. Bot will stop responding to messages

**To permanently remove:**
1. Delete the webhook:
   ```bash
   curl "https://api.telegram.org/bot<TOKEN>/deleteWebhook"
   ```
2. Delete the Pipedream workflow
3. Optional: Delete the bot with BotFather

---

## Cost Considerations

### Pipedream Free Tier

**Includes:**
- 100,000 credits per month
- Unlimited workflows
- Real-time logs (3-day retention)
- Standard execution time limits
- Community support

### Credit Consumption

**Typical usage per interaction:**

| Action | Credits | Notes |
|--------|---------|-------|
| `/start` command | 1-2 | Simple text response |
| Invalid message | 1-2 | Quick validation |
| YouTube download | 10-30 | Varies by video length |
| Audio transcription | 20-50 | Depends on audio duration |
| Error handling | 1-5 | Quick failure |

**Example monthly usage:**
- 500 `/start` commands: ~1,000 credits
- 200 YouTube downloads: ~4,000 credits
- 300 transcriptions: ~10,000 credits
- **Total:** ~15,000 credits (well within free tier)

### When to Upgrade

**Consider upgrading if:**
- You exceed 100,000 credits/month
- You need longer execution times (>60 seconds)
- You want longer log retention
- You need priority support
- Your bot has many users

### Paid Plans

**Pipedream offers paid tiers:**
- **Basic:** $19/month - More credits, longer executions
- **Advanced:** $49/month - Even more resources
- **Business:** Custom pricing - Enterprise features

Check [Pipedream Pricing](https://pipedream.com/pricing) for current details.

### Cost Optimization Tips

1. **Use smaller models:**
   - Tiny Whisper model is faster = fewer credits
   
2. **Reduce video quality:**
   - Lower quality = faster processing = fewer credits

3. **Implement caching:**
   - Don't reprocess the same content

4. **Add rate limiting:**
   - Prevent users from spamming the bot

5. **Handle errors efficiently:**
   - Quick failures consume fewer credits

6. **Monitor usage:**
   - Check usage dashboard regularly
   - Optimize expensive operations

---

## Advanced Configuration

### Using Pipedream Data Stores

To persist data between invocations:

```python
# Store user preferences
pd.data_store.set(f"user_{chat_id}_setting", "value")

# Retrieve user preferences
setting = pd.data_store.get(f"user_{chat_id}_setting")
```

### Custom Whisper Model Settings

Adjust transcription quality/speed:

```python
# Faster, less accurate
model = WhisperModel("tiny", device="cpu", compute_type="int8")

# Slower, more accurate
model = WhisperModel("small", device="cpu", compute_type="int8")

# Best quality (requires more resources)
model = WhisperModel("medium", device="cpu", compute_type="float16")
```

### Adding User Rate Limiting

Prevent abuse:

```python
# Track last request time per user
last_request = pd.data_store.get(f"last_request_{chat_id}")
if last_request:
    time_diff = time.time() - float(last_request)
    if time_diff < 5:  # 5 seconds cooldown
        await bot.send_message(
            chat_id=chat_id,
            text="Please wait a few seconds before sending another request."
        )
        return

pd.data_store.set(f"last_request_{chat_id}", str(time.time()))
```

### Implementing Usage Analytics

Track bot usage:

```python
# Increment usage counter
count = pd.data_store.get("total_requests") or 0
pd.data_store.set("total_requests", int(count) + 1)

# Track by feature
feature_count = pd.data_store.get(f"feature_{feature_name}") or 0
pd.data_store.set(f"feature_{feature_name}", int(feature_count) + 1)
```

### Multi-Language Support

Improve transcription for specific languages:

```python
# Specify language hint
segments, info = model.transcribe(
    audio_path,
    language="es",  # Spanish
    beam_size=5
)

# Or detect automatically (default)
segments, info = model.transcribe(audio_path)
# info.language will contain detected language
```

### Error Reporting Integration

Send errors to external service (e.g., Sentry):

```python
import sentry_sdk

sentry_sdk.init("your-sentry-dsn")

try:
    # Your code
except Exception as e:
    sentry_sdk.capture_exception(e)
    raise
```

### Adding More Commands

Extend bot functionality:

```python
async def _handle_text_message(self, update):
    text = update.message.text.strip()
    chat_id = update.message.chat_id
    
    if text.startswith('/start'):
        await self._send_start_message(chat_id)
    elif text.startswith('/help'):
        await self._send_help_message(chat_id)
    elif text.startswith('/stats'):
        await self._send_stats(chat_id)
    # ... etc
```

### Webhook Secret Token (Enhanced Security)

Use Telegram's secret token feature:

1. **Set webhook with secret:**
   ```bash
   curl "https://api.telegram.org/bot<TOKEN>/setWebhook?url=<URL>&secret_token=<YOUR_SECRET>"
   ```

2. **Validate in code:**
   ```python
   def handler(pd: "pipedream"):
       # Check X-Telegram-Bot-Api-Secret-Token header
       headers = pd.steps["trigger"]["event"].get("headers", {})
       secret = headers.get("X-Telegram-Bot-Api-Secret-Token")
       
       expected_secret = os.environ.get("WEBHOOK_SECRET")
       if secret != expected_secret:
           return {"statusCode": 403, "body": "Forbidden"}
   ```

---

## Additional Resources

### Documentation Links

- **Pipedream Docs:** [https://pipedream.com/docs](https://pipedream.com/docs)
- **Telegram Bot API:** [https://core.telegram.org/bots/api](https://core.telegram.org/bots/api)
- **python-telegram-bot:** [https://python-telegram-bot.readthedocs.io/](https://python-telegram-bot.readthedocs.io/)
- **yt-dlp:** [https://github.com/yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp)
- **faster-whisper:** [https://github.com/guillaumekln/faster-whisper](https://github.com/guillaumekln/faster-whisper)

### Related Guides in This Repository

- **[Quick Start Guide](QUICKSTART_PIPEDREAM.md)** - 5-minute quick setup
- **[Polling vs Webhook](POLLING_VS_WEBHOOK.md)** - Deployment mode comparison
- **[Architecture Overview](ARCHITECTURE.md)** - Technical architecture details
- **[Main README](README.md)** - Project overview and features

### Community and Support

- **Pipedream Community:** [https://pipedream.com/community](https://pipedream.com/community)
- **Telegram Bot Developers:** [https://t.me/BotDevelopment](https://t.me/BotDevelopment)
- **Stack Overflow:** Tag questions with `pipedream`, `telegram-bot`, `python`

### Video Tutorials

Search YouTube for:
- "Pipedream tutorial"
- "Telegram bot webhook Python"
- "Deploying bots to Pipedream"

---

## Troubleshooting Checklist

Before asking for help, verify:

- [ ] Pipedream account is created and verified
- [ ] Workflow is created with HTTP/Webhook trigger
- [ ] Python code from `pipedream_handler.py` is copied correctly
- [ ] All three dependencies are added (python-telegram-bot, yt-dlp, faster-whisper)
- [ ] `BOT_TOKEN` environment variable is set correctly (no spaces, no quotes)
- [ ] Workflow is deployed (green checkmark or "Deployed" status)
- [ ] Webhook URL is copied correctly
- [ ] Webhook is registered with Telegram (check with `getWebhookInfo`)
- [ ] `getWebhookInfo` shows your Pipedream URL
- [ ] `pending_update_count` in `getWebhookInfo` is 0
- [ ] Bot responds to `/start` command
- [ ] Logs show incoming webhook events
- [ ] No Python syntax errors in logs
- [ ] Bot token is from the correct bot

If all checks pass and bot still doesn't work, check the [Troubleshooting](#troubleshooting) section or review Pipedream logs for specific errors.

---

## Quick Reference

### Essential Commands

**Set webhook:**
```bash
curl "https://api.telegram.org/bot<TOKEN>/setWebhook?url=<URL>"
```

**Check webhook:**
```bash
curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"
```

**Delete webhook:**
```bash
curl "https://api.telegram.org/bot<TOKEN>/deleteWebhook"
```

**Test webhook manually:**
```bash
curl -X POST <PIPEDREAM_URL> \
  -H "Content-Type: application/json" \
  -d '{"update_id":1,"message":{"message_id":1,"from":{"id":123,"first_name":"Test"},"chat":{"id":123,"type":"private"},"text":"/start"}}'
```

### Environment Variables

| Variable | Required | Example |
|----------|----------|---------|
| `BOT_TOKEN` | Yes | `123456789:ABCdefGHI...` |
| `WEBHOOK_SECRET` | Optional | `my-secret-token` |

### Important URLs

- **Pipedream Dashboard:** `https://pipedream.com`
- **Telegram Bot API:** `https://api.telegram.org/bot<TOKEN>/`
- **BotFather:** `https://t.me/botfather`

### File Reference

- **`pipedream_handler.py`** - Main code to copy into Pipedream
- **`pipedream_webhook.py`** - Alternative implementation
- **`setup_webhook.sh`** - Helper script for webhook setup
- **`QUICKSTART_PIPEDREAM.md`** - 5-minute quick start guide

---

## Final Checklist

Before you finish:

✅ **Pipedream workflow created and deployed**  
✅ **Bot token added as environment variable**  
✅ **Python code copied from `pipedream_handler.py`**  
✅ **Dependencies added (python-telegram-bot, yt-dlp, faster-whisper)**  
✅ **Webhook URL copied**  
✅ **Webhook registered with Telegram**  
✅ **Webhook verified with `getWebhookInfo`**  
✅ **Bot responds to `/start` command**  
✅ **Logs show successful executions**  
✅ **Bot tested with YouTube URL (if FFmpeg available)**  
✅ **Bot tested with voice message**  

---

**Congratulations! Your Telegram bot is now live on Pipedream! 🎉**

If you encounter any issues, refer to the [Troubleshooting](#troubleshooting) section or check the Pipedream logs for detailed error messages.

For quick deployment, see [QUICKSTART_PIPEDREAM.md](QUICKSTART_PIPEDREAM.md).
