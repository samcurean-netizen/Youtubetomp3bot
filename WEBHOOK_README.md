# Webhook Implementation for Pipedream

Quick reference guide for the webhook-based deployment.

## 🚀 Quick Deploy (5 Minutes)

1. **Create Pipedream Workflow**
   - Go to https://pipedream.com/workflows
   - Click "New Workflow"
   - Select "HTTP / Webhook" trigger

2. **Add Python Code**
   - Add Python code step
   - Copy entire `pipedream_handler.py` file
   - Add dependencies: `python-telegram-bot`, `yt-dlp`, `faster-whisper`

3. **Configure**
   - Set `BOT_TOKEN` in environment variables
   - Deploy workflow
   - Copy webhook URL

4. **Set Webhook**
   ```bash
   export BOT_TOKEN="your-token"
   export WEBHOOK_URL="your-pipedream-url"
   ./setup_webhook.sh
   ```

5. **Test**
   - Send `/start` to your bot
   - Done! 🎉

## 📚 Documentation

- **[5-Minute Quick Start](QUICKSTART_PIPEDREAM.md)** - Fastest setup
- **[Complete Guide](PIPEDREAM_DEPLOYMENT.md)** - Detailed instructions
- **[Comparison](POLLING_VS_WEBHOOK.md)** - Polling vs Webhook
- **[Architecture](ARCHITECTURE.md)** - How it works
- **[Full Index](DOCS_INDEX.md)** - All documentation

## 📁 Key Files

### Must-Use
- `pipedream_handler.py` - Main webhook handler (copy to Pipedream)
- `setup_webhook.sh` - Automated webhook setup

### Supporting
- `test_webhook_handler.py` - Test locally before deploying
- `requirements-pipedream.txt` - Python dependencies
- `pipedream_workflow_example.yaml` - Workflow reference

### Documentation
- All `*.md` files - Comprehensive guides

## ✅ Features

All original bot features work identically:
- ✅ YouTube to MP3 downloads
- ✅ Audio transcription
- ✅ /start command
- ✅ Error handling
- ✅ File cleanup

Plus webhook benefits:
- ⚡ Instant response (no polling delay)
- 💰 Pay per use (free tier generous)
- 📈 Auto-scaling
- 🔧 No server maintenance

## 🧪 Testing

### Local Test
```bash
export BOT_TOKEN="your-token"
python test_webhook_handler.py
```

### Production Test
1. Deploy to Pipedream
2. Set webhook URL
3. Send messages to bot
4. Check Pipedream logs

## 💡 Tips

1. **Use Quick Start** - If experienced, jump straight to quick start
2. **Test Locally** - Use test script before deploying
3. **Check Logs** - Pipedream provides excellent logging
4. **Monitor Usage** - Track your credit usage
5. **Read Docs** - Comprehensive guides for deep dives

## 🆘 Common Issues

### Bot not responding?
```bash
# Check webhook status
curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"
```

### FFmpeg errors?
- Expected in some Pipedream environments
- Audio transcription still works
- YouTube downloads may need Docker workflow

### Need help?
- Check [PIPEDREAM_DEPLOYMENT.md](PIPEDREAM_DEPLOYMENT.md) troubleshooting
- Review Pipedream logs
- Verify BOT_TOKEN is set

## 💰 Cost

**Free tier:** 100,000 credits/month
- Enough for thousands of messages
- Typical bot uses 1-50 credits per request
- No credit card required

**Your bot will likely run free! 🎉**

## 🔗 Links

- [Pipedream](https://pipedream.com)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Documentation Index](DOCS_INDEX.md)

## 📞 Support

1. Read the documentation
2. Check Pipedream logs
3. Test locally
4. Review troubleshooting guides

---

**Ready to deploy? Start with [QUICKSTART_PIPEDREAM.md](QUICKSTART_PIPEDREAM.md)!**
