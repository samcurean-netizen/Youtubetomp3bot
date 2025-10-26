#!/usr/bin/env python3
"""
Test script for webhook handler.

This script simulates a webhook POST request from Telegram to test
the handler locally before deploying to Pipedream.

Usage:
    export BOT_TOKEN="your-token-here"
    python test_webhook_handler.py
"""

import asyncio
import json
import os
import sys


class MockPipedream:
    """Mock Pipedream context for testing."""
    
    def __init__(self, update_data):
        self.steps = {
            "trigger": {
                "event": {
                    "body": update_data
                }
            }
        }


async def test_start_command():
    """Test /start command."""
    print("\n" + "="*60)
    print("TEST 1: /start command")
    print("="*60)
    
    from pipedream_handler import handler
    
    update_data = {
        "update_id": 123456789,
        "message": {
            "message_id": 1,
            "from": {
                "id": 123456,
                "is_bot": False,
                "first_name": "Test",
                "username": "testuser"
            },
            "chat": {
                "id": 123456,
                "first_name": "Test",
                "username": "testuser",
                "type": "private"
            },
            "date": 1234567890,
            "text": "/start"
        }
    }
    
    pd = MockPipedream(update_data)
    result = await handler(pd)
    
    print(f"Result: {json.dumps(result, indent=2)}")
    assert result["statusCode"] == 200, "Expected status code 200"
    print("✅ Test passed!")


async def test_youtube_url():
    """Test YouTube URL processing."""
    print("\n" + "="*60)
    print("TEST 2: YouTube URL")
    print("="*60)
    print("Note: This will attempt to download a short YouTube video.")
    print("Make sure you have yt-dlp and FFmpeg installed.")
    
    response = input("Do you want to run this test? (y/n): ")
    if response.lower() != 'y':
        print("Skipping YouTube test")
        return
    
    from pipedream_handler import handler
    
    # Use a very short test video
    update_data = {
        "update_id": 123456790,
        "message": {
            "message_id": 2,
            "from": {
                "id": 123456,
                "is_bot": False,
                "first_name": "Test",
                "username": "testuser"
            },
            "chat": {
                "id": 123456,
                "first_name": "Test",
                "username": "testuser",
                "type": "private"
            },
            "date": 1234567891,
            "text": "https://www.youtube.com/watch?v=jNQXAC9IVRw"  # "Me at the zoo" - first YouTube video (18 seconds)
        }
    }
    
    pd = MockPipedream(update_data)
    result = await handler(pd)
    
    print(f"Result: {json.dumps(result, indent=2)}")
    print("Check Telegram to see if the MP3 was sent!")


async def test_invalid_url():
    """Test invalid URL."""
    print("\n" + "="*60)
    print("TEST 3: Invalid URL")
    print("="*60)
    
    from pipedream_handler import handler
    
    update_data = {
        "update_id": 123456791,
        "message": {
            "message_id": 3,
            "from": {
                "id": 123456,
                "is_bot": False,
                "first_name": "Test",
                "username": "testuser"
            },
            "chat": {
                "id": 123456,
                "first_name": "Test",
                "username": "testuser",
                "type": "private"
            },
            "date": 1234567892,
            "text": "This is just random text"
        }
    }
    
    pd = MockPipedream(update_data)
    result = await handler(pd)
    
    print(f"Result: {json.dumps(result, indent=2)}")
    assert result["statusCode"] == 200, "Expected status code 200"
    print("✅ Test passed!")


async def test_empty_body():
    """Test empty webhook body."""
    print("\n" + "="*60)
    print("TEST 4: Empty body")
    print("="*60)
    
    from pipedream_handler import handler
    
    pd = MockPipedream({})
    result = await handler(pd)
    
    print(f"Result: {json.dumps(result, indent=2)}")
    assert result["statusCode"] == 400, "Expected status code 400 for empty body"
    print("✅ Test passed!")


async def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("TELEGRAM BOT WEBHOOK HANDLER - TEST SUITE")
    print("="*60)
    
    # Check for BOT_TOKEN
    bot_token = os.environ.get('BOT_TOKEN')
    if not bot_token:
        print("\n❌ ERROR: BOT_TOKEN environment variable not set!")
        print("\nPlease set it first:")
        print("  export BOT_TOKEN='your-token-here'")
        print("\nOr for a quick test without actually sending messages:")
        print("  export BOT_TOKEN='dummy-token-for-testing'")
        sys.exit(1)
    
    print(f"\n✅ BOT_TOKEN found: {bot_token[:10]}...")
    
    # Run tests
    try:
        await test_start_command()
        await test_invalid_url()
        await test_empty_body()
        await test_youtube_url()  # Interactive test
        
        print("\n" + "="*60)
        print("ALL TESTS COMPLETED!")
        print("="*60)
        print("\n✅ Your webhook handler is working correctly!")
        print("\nNext steps:")
        print("1. Deploy to Pipedream")
        print("2. Set webhook URL with Telegram")
        print("3. Test with your actual bot")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    # Check if handler file exists
    try:
        import pipedream_handler
    except ImportError:
        print("❌ ERROR: Could not import pipedream_handler.py")
        print("Make sure you're running this from the project directory.")
        sys.exit(1)
    
    asyncio.run(main())
