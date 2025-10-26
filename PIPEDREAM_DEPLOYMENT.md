# Complete Pipedream Deployment Guide

This comprehensive guide will walk you through deploying your Telegram bot to Pipedream with webhooks, step by step. **No prior Pipedream or serverless experience required!**

---

## 📋 Table of Contents

1. [What is Pipedream?](#what-is-pipedream)
2. [How Webhooks Work](#how-webhooks-work)
3. [Prerequisites](#prerequisites)
4. [Step 1: Get Your Telegram Bot Token](#step-1-get-your-telegram-bot-token)
5. [Step 2: Create a Pipedream Account](#step-2-create-a-pipedream-account)
6. [Step 3: Create a New Workflow](#step-3-create-a-new-workflow)
7. [Step 4: Add Your Python Code](#step-4-add-your-python-code)
8. [Step 5: Configure Environment Variables](#step-5-configure-environment-variables)
9. [Step 6: Deploy Your Workflow](#step-6-deploy-your-workflow)
10. [Step 7: Get Your Webhook URL](#step-7-get-your-webhook-url)
11. [Step 8: Register Webhook with Telegram](#step-8-register-webhook-with-telegram)
12. [Step 9: Test Your Bot](#step-9-test-your-bot)
13. [Viewing Logs and Monitoring](#viewing-logs-and-monitoring)
14. [Troubleshooting](#troubleshooting)
15. [Maintenance and Updates](#maintenance-and-updates)
16. [Cost and Usage](#cost-and-usage)
17. [Advanced Configuration](#advanced-configuration)

---

## What is Pipedream?

**Pipedream** is a serverless platform that lets you run code in response to events (like HTTP requests) without managing servers. Think of it as a service that:
- Runs your code only when needed (when someone messages your bot)
- Handles scaling automatically
- Provides free hosting for moderate usage
- Shows real-time logs of every execution

**Why use Pipedream for your Telegram bot?**
- ✅ No server maintenance
- ✅ Automatic scaling
- ✅ Free tier (100,000 credits/month)
- ✅ Easy deployment
- ✅ Built-in monitoring and logs

---

## How Webhooks Work

Traditional bots use **polling** (constantly asking Telegram "got any new messages?"). With **webhooks**:

1. You give Telegram a URL (your Pipedream webhook)
2. When someone messages your bot, Telegram immediately sends a POST request to that URL
3. Pipedream receives it and runs your code
4. Your code processes the message and responds
5. Done! No continuous running needed.

**Benefits:**
- Lower resource usage (only runs when needed)
- Faster response times
- Better for serverless platforms

---

## Prerequisites

Before you begin, make sure you have:

- ✅ A computer with internet access
- ✅ A web browser (Chrome, Firefox, Safari, etc.)
- ✅ A Telegram account
- ✅ 20-30 minutes of time

**That's it!** No coding experience, servers, or payment required.

---

## Step 1: Get Your Telegram Bot Token

### What is a Bot Token?
A bot token is like a password that lets your code control your Telegram bot. It's a long string like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

### How to Get Your Token

**1. Open Telegram** on your phone or computer

**2. Search for "@BotFather"**
   - In the Telegram search bar, type: `@BotFather`
   - Select the official BotFather (it has a blue verified checkmark)

**3. Start a conversation**
   - Click "Start" or send `/start`

**4. Create a new bot**
   - Send the command: `/newbot`
   - BotFather will ask you for a name

**5. Choose a name for your bot**
   - Example: "My Audio Bot"
   - This is the display name users will see
   - Send your chosen name

**6. Choose a username**
   - Must end in "bot" (e.g., `my_audio_bot` or `MyAudioBot`)
   - Must be unique (not taken by another bot)
   - Example: `my_audio_helper_bot`
   - Send your chosen username

**7. Copy your token**
   - BotFather will reply with a message containing your token
   - It looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
   - **IMPORTANT**: Copy this entire token and save it somewhere safe
   - **Never share this token publicly** - it controls your bot!

**Optional: Customize your bot**
- `/setdescription` - Set a description users see before starting
- `/setabouttext` - Set an about text
- `/setuserpic` - Upload a profile picture

**Example conversation:**
```
You: /newbot
BotFather: Alright, a new bot. How are we going to call it? Please choose a name for your bot.

You: My Audio Bot
BotFather: Good. Now let's choose a username for your bot. It must end in `bot`. Like this, for example: TetrisBot or tetris_bot.

You: my_audio_helper_bot
BotFather: Done! Congratulations on your new bot. You will find it at t.me/my_audio_helper_bot. You can now add a description...

Use this token to access the HTTP API:
123456789:ABCdefGHIjklMNOpqrsTUVwxyz

For a description of the Bot API, see this page: https://core.telegram.org/bots/api
```

✅ **You now have your bot token! Keep it safe for Step 5.**

---

## Step 2: Create a Pipedream Account

**1. Go to Pipedream**
   - Open your browser
   - Visit: https://pipedream.com/auth/signup

**2. Sign up**
   - You can sign up with:
     - GitHub account (recommended)
     - Google account
     - Email address
   - Click your preferred signup method

**3. Complete signup**
   - If using GitHub/Google: Authorize the connection
   - If using email: Check your email for verification link

**4. Verify your account**
   - Follow the verification steps if prompted

**5. Welcome to Pipedream!**
   - You'll see the Pipedream dashboard
   - Don't worry if it looks unfamiliar - we'll walk through it

✅ **You now have a Pipedream account!**

**Note:** The free tier gives you 100,000 credits/month, which is plenty for a personal bot handling hundreds of messages daily.

---

## Step 3: Create a New Workflow

### What is a Workflow?
A workflow is like a container for your bot code. It includes:
- A trigger (what starts the code - in our case, HTTP requests from Telegram)
- Steps (the actual code that processes messages)
- Configuration (environment variables like your bot token)

### Creating the Workflow

**1. Navigate to Workflows**
   - From the Pipedream homepage, click "Workflows" in the left sidebar
   - Or go directly to: https://pipedream.com/workflows

**2. Create a New Workflow**
   - Click the green **"New Workflow"** button (top right)
   - A dialog will appear asking you to select a trigger

**3. Select HTTP Trigger**
   - In the search box, type: "HTTP"
   - You'll see several options
   - Click on **"HTTP / Webhook"**
   - Then select **"HTTP Requests"** (usually the first option)
   - Click **"Save and continue"** or similar button

**4. Configure the Trigger**
   - You'll see the trigger step added to your workflow
   - Default settings are fine - you don't need to change anything
   - The trigger will automatically accept POST requests (what Telegram sends)

**5. Name Your Workflow (Optional)**
   - At the top, you'll see "Untitled Workflow"
   - Click it to rename (e.g., "Telegram Audio Bot")
   - Or leave it as is - the name doesn't affect functionality

✅ **Your workflow now has an HTTP trigger that can receive webhook calls!**

**What you should see:**
- A workflow page with one step: "trigger" (HTTP / Webhook)
- The trigger shows a URL (we'll use this later)
- A "+" button below the trigger to add more steps

---

## Step 4: Add Your Python Code

### Which File to Use?
In the repository, you'll find a file called **`pipedream_handler.py`** - this is the complete bot code designed for Pipedream.

### Adding the Code Step

**1. Add a Code Step**
   - Below the trigger, click the **"+" button**
   - A menu appears with step options
   - Search for: "Python"
   - Select **"Run Python Code"**
   - Click to add it

**2. Open the Code Editor**
   - A new step appears called something like "run_python_code"
   - Click on this step to expand it
   - You'll see a code editor with some default Python code

**3. Get the Bot Code**
   - Open the repository where you downloaded/cloned this bot
   - Find the file: **`pipedream_handler.py`**
   - Open it in a text editor
   - Select all the contents (Ctrl+A or Cmd+A)
   - Copy it (Ctrl+C or Cmd+C)

**4. Paste the Code**
   - Go back to Pipedream
   - In the code editor, select all the default code (Ctrl+A or Cmd+A)
   - Delete it
   - Paste your copied code (Ctrl+V or Cmd+V)
   - The editor should now show the complete bot code

**5. Add Python Dependencies**
   - Scroll down in the code step
   - Look for a section called **"Packages"** or **"Python Packages"** or **"Add package"**
   - You need to add three packages. Click "Add package" for each:
     1. Type: `python-telegram-bot` → Select it (version 20.0 or higher)
     2. Click "Add package" again, type: `yt-dlp` → Select it
     3. Click "Add package" again, type: `faster-whisper` → Select it

**6. Verify**
   - Make sure all three packages show up in the packages list
   - The code editor should show your pasted code

✅ **Your bot code is now in Pipedream!**

**Troubleshooting:**
- If you can't find "Run Python Code", make sure you're clicking the "+" button below the trigger
- If packages don't autocomplete, you can type the exact name and version: `python-telegram-bot>=20.0`

---

## Step 5: Configure Environment Variables

### What are Environment Variables?
Environment variables are a secure way to store sensitive information (like your bot token) without putting it directly in the code.

### Adding Your Bot Token

**1. Open Settings**
   - Look at the top-right corner of your workflow page
   - You'll see several icons
   - Click the **gear/cog icon** (⚙️) - this is "Settings"

**2. Find Environment Variables**
   - In the settings panel that opens on the right
   - Look for a section called **"Environment Variables"** or **"Environment"**
   - Click on it to expand if needed

**3. Add New Variable**
   - Click **"Add environment variable"** or similar button
   - You'll see two fields: Name and Value

**4. Enter Your Bot Token**
   - **Name field**: Type exactly `BOT_TOKEN` (all caps, with underscore)
   - **Value field**: Paste your Telegram bot token (from Step 1)
   - Example value: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

**5. Save the Variable**
   - Click **"Save"** or **"Add"** button
   - The variable should now appear in your list

**6. Close Settings**
   - Click outside the settings panel or click the X to close it
   - Your environment variable is now configured

✅ **Your bot token is securely stored!**

**Security Notes:**
- Never commit your bot token to GitHub or share it publicly
- Pipedream encrypts environment variables
- If your token is ever leaked, use BotFather's `/revoke` command to get a new one

**Common Mistakes:**
- ❌ `bot_token` (lowercase) - Won't work! Must be `BOT_TOKEN`
- ❌ `BOT TOKEN` (with space) - Won't work! Must use underscore: `BOT_TOKEN`
- ❌ Including quotes around the token - Just paste the token itself, no quotes

---

## Step 6: Deploy Your Workflow

### What Does Deploying Mean?
Deploying activates your workflow so it can receive real requests. Before deployment, the workflow is in "draft" mode.

### How to Deploy

**1. Find the Deploy Button**
   - Look at the top-right corner of the workflow page
   - You'll see a button that says **"Deploy"**
   - It might be blue or green

**2. Click Deploy**
   - Click the **"Deploy"** button
   - Pipedream will start deploying your workflow
   - You'll see a progress indicator or loading animation

**3. Wait for Deployment**
   - This usually takes 10-30 seconds
   - Pipedream is:
     - Installing the Python packages you specified
     - Setting up the environment
     - Making your workflow live

**4. Deployment Complete**
   - You'll see a success message or checkmark
   - The "Deploy" button might change to show it's live
   - A green dot or "Active" status appears

✅ **Your workflow is now live and ready to receive webhooks!**

**What if deployment fails?**
- Check if all three Python packages were added correctly
- Verify that the code was pasted completely
- Look for any error messages - they usually indicate what's wrong
- Most common issue: package names misspelled

---

## Step 7: Get Your Webhook URL

### What is the Webhook URL?
This is the public URL that Telegram will use to send messages to your bot. Every Pipedream workflow gets a unique URL.

### Finding Your URL

**1. Locate the Trigger Step**
   - Scroll to the top of your workflow
   - Find the first step (the HTTP / Webhook trigger)
   - Click on it to expand if it's collapsed

**2. Find the URL**
   - In the trigger step, look for a section that says:
     - "Webhook URL" or
     - "Endpoint URL" or
     - Just "URL"
   - You'll see a URL that looks like: `https://eo123abc.m.pipedream.net`
   - The exact subdomain (eo123abc) will be different for you

**3. Copy the URL**
   - Click the copy icon next to the URL, or
   - Select the entire URL and copy it (Ctrl+C or Cmd+C)
   - The URL should be in your clipboard now

**4. Save the URL**
   - Paste it somewhere safe (like a text file or note)
   - You'll need this URL in the next step

✅ **You have your webhook URL!**

**Example URLs:**
- `https://eo123abc.m.pipedream.net`
- `https://en456def.m.pipedream.net`
- All Pipedream webhook URLs follow this pattern: `https://[random].m.pipedream.net`

**Note:** This URL is public but only processes valid Telegram updates. It's safe to use.

---

## Step 8: Register Webhook with Telegram

### What is Webhook Registration?
You need to tell Telegram where to send updates for your bot. This is called "setting the webhook."

### Prerequisites
- Your bot token (from Step 1)
- Your Pipedream webhook URL (from Step 7)

### Method 1: Using the Setup Script (Easiest)

If you have the repository downloaded on your computer:

**1. Open Terminal/Command Prompt**
   - **Mac/Linux**: Open Terminal
   - **Windows**: Open Command Prompt or PowerShell

**2. Navigate to the Repository**
   ```bash
   cd /path/to/telegram-audio-bot
   ```

**3. Run the Setup Script**
   ```bash
   ./setup_webhook.sh
   ```

**4. Enter Your Details**
   - When prompted, paste your bot token
   - Press Enter
   - When prompted, paste your Pipedream webhook URL
   - Press Enter

**5. Verify Success**
   - The script will show you the result
   - You should see: `✅ Webhook set successfully!`

### Method 2: Using cURL (Command Line)

**1. Open Terminal/Command Prompt**

**2. Run This Command** (replace the placeholders):
```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=<YOUR_PIPEDREAM_URL>"
```

**Example with real values:**
```bash
curl "https://api.telegram.org/bot123456789:ABCdefGHIjklMNOpqrsTUVwxyz/setWebhook?url=https://eo123abc.m.pipedream.net"
```

**3. Check the Response**
You should see:
```json
{"ok":true,"result":true,"description":"Webhook was set"}
```

### Method 3: Using Your Web Browser (No Command Line Needed!)

**1. Build Your URL**
Take this template:
```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=<YOUR_PIPEDREAM_URL>
```

**2. Replace the Placeholders**
- Replace `<YOUR_BOT_TOKEN>` with your actual bot token
- Replace `<YOUR_PIPEDREAM_URL>` with your actual Pipedream URL

**Example:**
```
https://api.telegram.org/bot123456789:ABCdefGHIjklMNOpqrsTUVwxyz/setWebhook?url=https://eo123abc.m.pipedream.net
```

**3. Paste in Browser**
- Copy your complete URL
- Paste it into your browser's address bar
- Press Enter

**4. Check the Response**
Your browser will show a JSON response:
```json
{"ok":true,"result":true,"description":"Webhook was set"}
```

If `"ok":true` appears, you're successful! ✅

### Verifying the Webhook

To verify your webhook is set correctly:

**Browser method:**
```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo
```

**cURL method:**
```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
```

**Expected Response:**
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

**What to check:**
- ✅ `"url"` matches your Pipedream URL
- ✅ `"pending_update_count": 0` (means no queued messages)
- ✅ No `"last_error_message"` field (would indicate problems)

### Removing Old Webhooks

If you previously had a webhook or polling bot:

**1. Delete any existing webhook:**
```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/deleteWebhook"
```

Or in browser:
```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/deleteWebhook
```

**2. Stop any polling bots:**
- If you had a bot running with polling, stop it
- Only one method (webhook OR polling) can be active

✅ **Your webhook is now registered with Telegram!**

---

## Step 9: Test Your Bot

Now for the exciting part - testing your bot!

### Basic Tests

**1. Open Telegram**
   - Open Telegram on your phone or computer

**2. Find Your Bot**
   - Search for your bot's username (e.g., `@my_audio_helper_bot`)
   - Or use the link from BotFather (e.g., `t.me/my_audio_helper_bot`)
   - Click on your bot

**3. Start the Bot**
   - Click "Start" button or send: `/start`
   - **Expected response:**
     ```
     Hi! I can help you with:
     🎵 Send me a YouTube link and I'll convert it to MP3
     🎤 Send me a voice message or audio file and I'll transcribe it

     All transcription happens locally - no external APIs needed!
     ```

✅ **If you see this message, your bot is working!**

### Test YouTube Download

**1. Find a YouTube video**
   - Go to YouTube
   - Pick any video
   - Copy the URL (e.g., `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)

**2. Send to Your Bot**
   - Paste the YouTube URL in your chat with the bot
   - Send it

**3. Watch the Bot Work**
   - You'll see: `⏳ Downloading...`
   - Then: `📤 Uploading MP3...`
   - Finally: The bot sends you an MP3 file!

**Expected time:** 10-60 seconds depending on video length

**Note:** This requires FFmpeg, which may not be available in all Pipedream environments. See [Troubleshooting](#troubleshooting) if this doesn't work.

### Test Audio Transcription

**1. Send a Voice Message**
   - In your chat with the bot
   - Hold the microphone button
   - Record a short message
   - Release to send

**2. Watch the Bot Transcribe**
   - You'll see: `⏳ Transcribing audio...`
   - After a few seconds: The transcribed text appears!

**Example:**
```
📝 Transcription (en):

Hello this is a test of the transcription feature. It should convert my speech to text.
```

**3. Try an Audio File (Optional)**
   - Send any audio file (.mp3, .m4a, .ogg, etc.)
   - The bot will transcribe it

✅ **All features are working!**

### What if Something Doesn't Work?

See the [Troubleshooting](#troubleshooting) section below.

---

## Viewing Logs and Monitoring

### Why Check Logs?
Logs show you exactly what's happening inside your bot - useful for debugging or monitoring usage.

### Accessing Logs

**1. Go to Your Workflow**
   - Open Pipedream
   - Navigate to your workflow

**2. Click the Logs Tab**
   - Near the top, you'll see tabs: "Build", "Logs", "Settings", etc.
   - Click on **"Logs"** or **"Events"**

**3. View Executions**
   - You'll see a list of every time your workflow ran
   - Each entry represents one message to your bot
   - Click on any entry to see full details

### Understanding Log Entries

**What you'll see:**
- **Timestamp**: When the request came in
- **Status**: Success (200) or error
- **Duration**: How long it took to process
- **Data**: The full request and response

**Example log entry:**
```
✅ 2024-03-15 10:30:45 - Status: 200
Duration: 2.3s
Trigger: HTTP Request
Body: {"update_id": 123456, "message": {...}}
```

**Click on an entry to see:**
- Full request body from Telegram
- Each step's output
- Console logs (your code's print/log statements)
- Any errors that occurred

### Real-Time Monitoring

**1. Keep Logs Tab Open**
   - New executions appear automatically
   - No need to refresh

**2. Send a Test Message**
   - Message your bot in Telegram
   - Watch the log appear in Pipedream in real-time
   - Click to see full details

**3. Check for Errors**
   - Red/failed entries indicate errors
   - Click them to see what went wrong
   - Usually shows the error message and stack trace

✅ **You can now monitor your bot in real-time!**

### Key Things to Monitor

- **Execution time**: Should be under 30 seconds (free tier limit)
- **Error rate**: Occasional errors are normal, frequent errors need investigation
- **Credit usage**: Check your account's credit consumption
- **Pending updates**: In webhook info, should be 0

---

## Troubleshooting

### Bot Not Responding to Messages

**Symptom:** You send `/start` but nothing happens.

**Checklist:**

1. **Is the webhook set?**
   ```bash
   curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"
   ```
   - ✅ `"url"` should show your Pipedream URL
   - ❌ If empty, run Step 8 again

2. **Is the workflow deployed?**
   - Go to your Pipedream workflow
   - Look for green "Active" or "Deployed" indicator
   - ❌ If not, click "Deploy"

3. **Is BOT_TOKEN set correctly?**
   - Workflow → Settings → Environment Variables
   - Check `BOT_TOKEN` value
   - Verify no extra spaces or quotes
   - ❌ Fix and redeploy

4. **Check Pipedream logs:**
   - Go to Logs tab
   - Send a test message to your bot
   - Do you see a new log entry?
   - ✅ Entry appears: Click it to see error details
   - ❌ No entry: Webhook isn't reaching Pipedream

5. **Is another bot/webhook active?**
   - Only one webhook per bot token
   - Delete old webhook: `deleteWebhook` endpoint
   - Stop any polling bots

6. **Try re-setting the webhook:**
   ```bash
   # Delete old webhook
   curl "https://api.telegram.org/bot<TOKEN>/deleteWebhook"
   
   # Wait 2 seconds
   
   # Set new webhook
   curl "https://api.telegram.org/bot<TOKEN>/setWebhook?url=<PIPEDREAM_URL>"
   ```

### YouTube Download Failing

**Symptom:** Bot responds to YouTube links with an error.

**Common Causes:**

1. **FFmpeg Not Available**
   
   **Symptom:** Error message mentions "ffmpeg not found" or "FFmpeg not installed"
   
   **Why:** Pipedream's Python environment may not include FFmpeg
   
   **Solutions:**
   
   **Option A: Wait for updates** (Easiest)
   - Pipedream may add FFmpeg support in the future
   - Check Pipedream's documentation
   
   **Option B: Use a Docker-based workflow** (Advanced)
   - Create a workflow using a custom Docker container
   - Include FFmpeg in your Dockerfile
   - Example Dockerfile:
     ```dockerfile
     FROM python:3.11-slim
     
     RUN apt-get update && apt-get install -y \
         ffmpeg \
         && rm -rf /var/lib/apt/lists/*
     
     COPY requirements.txt .
     RUN pip install -r requirements.txt
     
     COPY pipedream_handler.py .
     ```
   - See [Pipedream Docker workflows documentation](https://pipedream.com/docs/workflows/docker/)
   
   **Option C: Use static FFmpeg binary** (Advanced)
   - Download a static FFmpeg binary for Linux
   - Include it in your workflow
   - Update PATH in your code
   - Not recommended for beginners

2. **Video Too Long**
   
   **Symptom:** Timeout error after 30-60 seconds
   
   **Why:** Free tier has execution time limits
   
   **Solutions:**
   - Try shorter videos (under 10 minutes)
   - Upgrade to Pipedream paid plan for longer timeouts
   - Reduce quality in yt-dlp options:
     ```python
     'preferredquality': '128',  # Lower from 192
     ```

3. **Invalid URL**
   
   **Symptom:** "Please send a valid YouTube link"
   
   **Solutions:**
   - Check URL is from youtube.com or youtu.be
   - Try a different video
   - Make sure URL is not a playlist or channel

4. **yt-dlp Issues**
   
   **Symptom:** Error about video extraction
   
   **Solutions:**
   - Some videos are region-restricted
   - Some videos are age-restricted
   - Try a different video
   - Check if video is still available

### Transcription Not Working

**Symptom:** Voice messages show error or timeout.

**Solutions:**

1. **Model Download Timeout**
   
   **First run:** The Whisper model downloads (~150MB for base model)
   - This can take 30+ seconds
   - May timeout on free tier
   - Subsequent runs will be faster (model is cached)
   
   **Solution:** Upgrade to paid plan or use smaller model:
   ```python
   WhisperModel("tiny", device="cpu", compute_type="int8")
   ```

2. **Audio File Too Long**
   
   **Solution:** 
   - Keep audio under 5 minutes
   - Use smaller Whisper model
   - Upgrade Pipedream plan

3. **Out of Memory**
   
   **Solution:**
   - Use smaller model (tiny instead of base)
   - Upgrade to higher memory tier

### "Configuration Error: BOT_TOKEN not set"

**Symptom:** This error in Pipedream logs.

**Solutions:**

1. **Add BOT_TOKEN:**
   - Workflow → Settings (gear icon) → Environment Variables
   - Add: Name = `BOT_TOKEN`, Value = your token
   - Click Save
   - Click "Deploy" to redeploy

2. **Check spelling:**
   - Must be exactly `BOT_TOKEN` (all caps, underscore)
   - Not `bot_token` or `BOT TOKEN`

3. **Redeploy:**
   - After adding variable, click "Deploy"

### Webhook Shows Errors in getWebhookInfo

**Symptom:** `"last_error_message"` field appears in webhook info.

**Common errors:**

1. **"Wrong response from the webhook: 500 Internal Server Error"**
   - Your code has an error
   - Check Pipedream logs for details
   - Fix the error and redeploy

2. **"Connection timed out"**
   - Your workflow took too long to respond
   - Optimize code or upgrade plan

3. **"Bad Request: invalid webhook URL"**
   - URL is malformed
   - Make sure you copied the full Pipedream URL
   - Reset webhook with correct URL

### "Empty webhook body" in Logs

**Symptom:** Logs show "Empty body" message.

**Cause:** The trigger received a request with no data.

**Solutions:**
- Ignore these - they're often from bots/scanners
- Telegram's real requests always have data
- Only worry if ALL requests show this

### Persistent Issues

If none of the above helps:

1. **Check Dependencies:**
   - Workflow → Code Step → Packages
   - Verify all three packages are listed:
     - python-telegram-bot
     - yt-dlp  
     - faster-whisper

2. **Re-paste Code:**
   - Maybe code didn't paste completely
   - Delete all code in editor
   - Re-paste from `pipedream_handler.py`

3. **Create New Workflow:**
   - Sometimes starting fresh helps
   - Create a new workflow
   - Follow all steps again

4. **Check Pipedream Status:**
   - Visit: https://pipedream.com/status
   - Ensure no ongoing incidents

5. **Ask for Help:**
   - Pipedream Community: https://pipedream.com/community
   - Include:
     - Error message from logs
     - What you've tried
     - Screenshots (without exposing token)

---

## Maintenance and Updates

### Updating Your Bot Code

**When you need to update:**
- Fix a bug
- Add new features
- Change bot behavior

**How to update:**

1. **Edit the code:**
   - Go to your workflow in Pipedream
   - Click on the Python code step
   - Make your changes in the editor

2. **Test changes (optional):**
   - Use the "Test" button if available
   - Or deploy and test with real messages

3. **Deploy:**
   - Click "Deploy" to activate changes
   - Old code is replaced immediately

4. **Verify:**
   - Send a test message
   - Check logs to confirm new code is running

### Monitoring Usage

**Check Credit Usage:**

1. Go to your [Pipedream account settings](https://pipedream.com/settings/billing)
2. See "Usage" or "Credits"
3. View current month's consumption

**Typical consumption:**
- Simple message (like /start): ~1-2 credits
- YouTube download (5-min video): ~10-20 credits
- Transcription (2-min audio): ~20-30 credits

**Free tier:** 100,000 credits/month
- ~5,000 simple messages
- ~500 YouTube downloads
- ~300 transcriptions

### Viewing Execution History

1. Go to workflow → Logs tab
2. See all executions (last 30 days on free tier)
3. Filter by date, status, duration
4. Export logs if needed

### Pause or Disable Bot

**Temporary (keep configuration):**

1. **Disable workflow:**
   - Workflow → Settings → Disable
   - Webhook stops processing requests
   - Re-enable anytime

2. **Or remove webhook:**
   ```bash
   curl "https://api.telegram.org/bot<TOKEN>/deleteWebhook"
   ```
   - Bot stops responding
   - Set webhook again to re-enable

**Permanent:**
- Delete workflow in Pipedream
- Revoke bot token with BotFather (`/revoke`)

### Backup Your Workflow

**Export code:**
1. Copy code from Python step
2. Save to local file
3. Store environment variables separately (in password manager)

**Recreate if needed:**
- Create new workflow
- Paste code
- Add environment variables
- Deploy

---

## Cost and Usage

### Pipedream Free Tier

**What you get:**
- ✅ 100,000 credits/month
- ✅ 30-day log retention
- ✅ 1 concurrent execution per workflow
- ✅ 30 second execution timeout
- ✅ 512 MB memory
- ✅ No credit card required

**What it costs:**
- **$0** for moderate usage
- Most personal bots stay well within free tier

### Understanding Credits

Each workflow execution consumes credits based on:
- **Execution time:** Longer = more credits
- **Memory used:** More memory = more credits
- **Number of steps:** More steps = more credits

**Approximate costs:**

| Action | Duration | Credits |
|--------|----------|---------|
| /start command | 0.5s | 1-2 |
| Simple text message | 0.5s | 1-2 |
| YouTube download (5 min) | 15-20s | 10-20 |
| Audio transcription (2 min) | 10-15s | 20-30 |
| Voice message transcription | 5-10s | 10-20 |

**Example monthly usage:**
- 100 /start commands = 200 credits
- 50 YouTube downloads = 750 credits
- 100 transcriptions = 2,500 credits
- **Total: ~3,500 credits/month**
- **Well within the 100,000 free credits! ✅**

### When You Might Need to Upgrade

**Paid plans start at $20/month** and include:
- 200,000+ credits
- Longer execution timeouts (up to 5 minutes)
- More memory
- 90-day log retention
- Priority support

**You might need paid plan if:**
- Processing very long videos (10+ minutes)
- High volume (1000+ messages/day)
- Long audio transcriptions (10+ minutes)
- Complex processing that takes time

**For most users:** Free tier is plenty! 🎉

### Optimizing Credit Usage

**Tips to stay in free tier:**

1. **Efficient error handling:**
   - Return errors quickly
   - Don't retry failed operations automatically

2. **Smaller Whisper model:**
   - Use `tiny` instead of `base`
   - Faster = fewer credits

3. **Set limits:**
   - Reject files over certain size
   - Limit video length

4. **Monitor usage:**
   - Check Pipedream billing page monthly
   - See which operations use most credits

---

## Advanced Configuration

### Using Pipedream Data Stores

Pipedream offers key-value storage for persistence across executions.

**Use case:** Track user preferences, rate limiting, statistics.

**Example:**
```python
# In your handler code
def handler(pd: "pipedream"):
    # Store data
    pd.flow.set("user_123_count", 5)
    
    # Retrieve data
    count = pd.flow.get("user_123_count", default=0)
    
    # Increment
    pd.flow.set("user_123_count", count + 1)
```

**Limitations:**
- Free tier: 10,000 keys per account
- Each key: up to 1 KB
- Use for small data only

### Custom Webhook Validation

Add security by validating requests are from Telegram:

**Option 1: IP Whitelist** (check Telegram's IP ranges)

**Option 2: Secret Token** (Telegram Bot API 6.0+)
```python
# When setting webhook, add secret token:
# setWebhook?url=...&secret_token=YOUR_SECRET

# In handler, verify:
secret = pd.steps["trigger"]["headers"]["X-Telegram-Bot-Api-Secret-Token"]
if secret != os.environ.get("WEBHOOK_SECRET"):
    return {"statusCode": 403, "body": "Forbidden"}
```

### Using External Databases

For complex bots, use external database:

**Options:**
- PostgreSQL (Heroku, Railway, Supabase)
- MongoDB (MongoDB Atlas)
- Redis (Redis Cloud)

**Add to code:**
```python
import os
import psycopg2

# In handler
conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
# Use database...
```

**Add connection string to environment variables:**
- Name: `DATABASE_URL`
- Value: `postgresql://user:pass@host/db`

### Multiple Bots on One Account

You can run multiple bot workflows:

1. Create separate workflow for each bot
2. Each gets its own webhook URL
3. Each has its own BOT_TOKEN environment variable
4. Credits shared across all workflows

### Using Different Whisper Models

Edit the code to change transcription accuracy/speed:

**In `pipedream_handler.py`, find:**
```python
WhisperModel("base", device="cpu", compute_type="int8")
```

**Change to:**
```python
# Faster, less accurate:
WhisperModel("tiny", device="cpu", compute_type="int8")

# Slower, more accurate:
WhisperModel("small", device="cpu", compute_type="int8")
```

**Model comparison:**

| Model | Size | Speed | Accuracy | Best For |
|-------|------|-------|----------|----------|
| tiny | 75 MB | Fastest | Lower | Quick responses, clear audio |
| base | 150 MB | Fast | Good | **Default - balanced** |
| small | 500 MB | Medium | Better | High accuracy needs |
| medium | 1.5 GB | Slow | High | Professional use |
| large | 3 GB | Slowest | Best | Maximum accuracy |

**Note:** Larger models may timeout on free tier.

### Custom Download Options

Modify YouTube download behavior:

**In `pipedream_handler.py`, find `ydl_opts` and customize:**

```python
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '128',  # Lower for smaller files
    }],
    'outtmpl': str(self.temp_dir / '%(title)s.%(ext)s'),
    'quiet': True,
    'no_warnings': True,
    'max_filesize': 50 * 1024 * 1024,  # 50 MB max
}
```

---

## Migration from Polling

If you're switching from a polling bot (like `main.py`):

### Steps to Migrate

**1. Stop the old bot:**
- If running on Replit/VPS, stop the process
- Close the terminal/tab running `python main.py`

**2. Remove old webhook (if any):**
```bash
curl "https://api.telegram.org/bot<TOKEN>/deleteWebhook"
```

**3. Wait 5 seconds**
- Ensure old bot is completely stopped

**4. Deploy Pipedream webhook** (follow this guide)

**5. Set new webhook:**
```bash
curl "https://api.telegram.org/bot<TOKEN>/setWebhook?url=<PIPEDREAM_URL>"
```

**6. Test thoroughly:**
- Send /start
- Try all features
- Monitor logs for errors

### Data Migration

**If you used the SQLite database:**
- Database (`bot_data.db`) only exists in polling version
- Webhook version doesn't persist database between runs
- Options:
  1. **Start fresh** (simplest)
  2. **Use Pipedream Data Stores** for key data
  3. **Use external database** (PostgreSQL, etc.)

### Differences to Note

| Feature | Polling (main.py) | Webhook (Pipedream) |
|---------|-------------------|---------------------|
| Database | SQLite, persists | Not persistent |
| Settings | Saved per-chat | Simplified |
| Keep-alive | Flask server | Not needed |
| Scaling | Manual | Automatic |
| Logs | stdout/file | Pipedream UI |
| Cost | Server costs | Free tier/credits |

---

## Support and Resources

### Official Documentation

- **Pipedream:** https://pipedream.com/docs
- **Telegram Bot API:** https://core.telegram.org/bots/api
- **python-telegram-bot:** https://python-telegram-bot.readthedocs.io/
- **yt-dlp:** https://github.com/yt-dlp/yt-dlp
- **faster-whisper:** https://github.com/guillaumekln/faster-whisper

### Getting Help

**Pipedream Community:**
- Forum: https://pipedream.com/community
- Discord: https://pipedream.com/support

**This Repository:**
- Check other documentation files:
  - [QUICKSTART_PIPEDREAM.md](QUICKSTART_PIPEDREAM.md) - 5-minute quick start
  - [POLLING_VS_WEBHOOK.md](POLLING_VS_WEBHOOK.md) - Comparison guide
  - [ARCHITECTURE.md](ARCHITECTURE.md) - Technical details

**Telegram Bot Help:**
- @BotFather - Bot management
- @BotSupport - Official support channel

### Common Questions

**Q: Can I use a custom domain for the webhook?**
A: Yes, Pipedream paid plans support custom domains. Free tier uses `*.m.pipedream.net`.

**Q: How do I know if I'm running out of credits?**
A: Check https://pipedream.com/settings/billing - it shows current month usage and sends email alerts.

**Q: Can I run multiple bots?**
A: Yes! Create separate workflows for each bot, each with its own BOT_TOKEN.

**Q: Is my bot token secure?**
A: Yes - Pipedream encrypts environment variables. Never commit tokens to GitHub.

**Q: Can I download the bot code to run locally later?**
A: Yes! The code in `pipedream_handler.py` can be adapted for other serverless platforms or local use.

**Q: What happens if I exceed free tier?**
A: Workflows stop executing until next month or you upgrade. No surprise charges.

**Q: Can I see who uses my bot?**
A: Yes - check Pipedream logs. Each message shows the user/chat ID.

**Q: How do I delete my bot?**
A: Tell @BotFather: `/deletebot` and select your bot. Also delete the Pipedream workflow.

---

## Quick Reference

### Essential Commands

**Check webhook status:**
```bash
curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"
```

**Set webhook:**
```bash
curl "https://api.telegram.org/bot<TOKEN>/setWebhook?url=<URL>"
```

**Delete webhook:**
```bash
curl "https://api.telegram.org/bot<TOKEN>/deleteWebhook"
```

### Files in Repository

| File | Purpose |
|------|---------|
| `pipedream_handler.py` | **Main bot code for Pipedream** ← Use this! |
| `pipedream_webhook.py` | Alternative implementation |
| `main.py` | Polling version (not for Pipedream) |
| `setup_webhook.sh` | Helper script to set webhook |
| `requirements-pipedream.txt` | Python dependencies list |
| `QUICKSTART_PIPEDREAM.md` | 5-minute quick start |
| This file | Complete deployment guide |

### Required Environment Variables

| Name | Value | Where |
|------|-------|-------|
| `BOT_TOKEN` | Your Telegram bot token | Workflow → Settings → Environment Variables |

### Required Python Packages

Add in Pipedream code step → Packages:
1. `python-telegram-bot` (version 20.0+)
2. `yt-dlp`
3. `faster-whisper`

---

## Conclusion

**Congratulations! 🎉** 

You now have a fully functional Telegram bot running on Pipedream with:
- ✅ YouTube to MP3 conversion
- ✅ Audio transcription
- ✅ Serverless deployment
- ✅ Automatic scaling
- ✅ Real-time logging
- ✅ Free hosting

### Next Steps

- **Customize:** Edit the code to add features
- **Monitor:** Check logs regularly
- **Share:** Give your bot to friends
- **Expand:** Add more commands and functionality
- **Learn:** Explore Pipedream's other features

### Feedback

Found this guide helpful? Have suggestions? 
- Star the repository
- Open an issue for improvements
- Contribute enhancements

---

**Happy bot building! 🤖🚀**
