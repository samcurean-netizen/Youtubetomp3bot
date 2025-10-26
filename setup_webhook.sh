#!/bin/bash

# Telegram Bot Webhook Setup Script
# This script helps you set up the webhook for your Telegram bot on Pipedream

set -e

echo "🤖 Telegram Bot Webhook Setup"
echo "=============================="
echo ""

# Check if BOT_TOKEN is provided
if [ -z "$BOT_TOKEN" ]; then
    echo "Please enter your Telegram Bot Token:"
    read -r BOT_TOKEN
fi

if [ -z "$BOT_TOKEN" ]; then
    echo "❌ Error: Bot token is required!"
    exit 1
fi

# Check if WEBHOOK_URL is provided
if [ -z "$WEBHOOK_URL" ]; then
    echo ""
    echo "Please enter your Pipedream webhook URL:"
    echo "(Example: https://eo123abc.m.pipedream.net)"
    read -r WEBHOOK_URL
fi

if [ -z "$WEBHOOK_URL" ]; then
    echo "❌ Error: Webhook URL is required!"
    exit 1
fi

echo ""
echo "📡 Setting webhook..."
echo "Bot Token: ${BOT_TOKEN:0:10}..."
echo "Webhook URL: $WEBHOOK_URL"
echo ""

# Set the webhook
RESPONSE=$(curl -s -X POST \
    "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook" \
    -d "url=${WEBHOOK_URL}" \
    -d "allowed_updates=[\"message\",\"callback_query\"]")

echo "Response: $RESPONSE"
echo ""

# Check if successful
if echo "$RESPONSE" | grep -q '"ok":true'; then
    echo "✅ Webhook set successfully!"
else
    echo "❌ Failed to set webhook. Please check the error message above."
    exit 1
fi

echo ""
echo "📊 Getting webhook info..."
INFO=$(curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getWebhookInfo")
echo "$INFO" | python3 -m json.tool 2>/dev/null || echo "$INFO"

echo ""
echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Make sure your Pipedream workflow is deployed"
echo "2. Ensure BOT_TOKEN is set in Pipedream environment variables"
echo "3. Test your bot by sending /start"
echo ""
