#!/usr/bin/env python3
"""Test script for Typefully MCP server - Read operations only."""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from dotenv import load_dotenv
    # Load environment variables
    load_dotenv()
except ImportError:
    print("dotenv not available, skipping environment loading")

from typefully_mcp_server.client import TypefullyClient


async def test_read_operations():
    """Test read operations with the real Typefully API."""
    print("🧪 Testing Typefully API Read Operations")
    print("=" * 50)
    
    # Check for API key
    api_key = os.getenv("TYPEFULLY_API_KEY")
    if not api_key or api_key == "your_typefully_api_key_here":
        print("❌ Error: Please set your real TYPEFULLY_API_KEY in the .env file")
        print("\n📝 Steps to get your API key:")
        print("1. Go to https://typefully.com")
        print("2. Navigate to Settings > Integrations")
        print("3. Generate an API key")
        print("4. Update the .env file with: TYPEFULLY_API_KEY=your_actual_key")
        return
    
    print("✅ API key found and configured")
    
    try:
        async with TypefullyClient() as client:
            print("\n📅 Testing get_scheduled_drafts...")
            try:
                scheduled = await client.get_scheduled_drafts()
                print(f"✅ Success! Found {len(scheduled)} scheduled drafts")
                
                if scheduled:
                    print("\n📋 First few scheduled drafts:")
                    for i, draft in enumerate(scheduled[:3], 1):
                        print(f"  {i}. ID: {draft.id}")
                        print(f"     First tweet: {draft.text_first_tweet[:60]}...")
                        print(f"     Tweets: {draft.num_tweets}")
                        if draft.scheduled_date:
                            print(f"     Scheduled: {draft.scheduled_date}")
                        print()
                else:
                    print("📝 No scheduled drafts found")
            except Exception as e:
                print(f"❌ Error getting scheduled drafts: {str(e)}")
            
            print("\n✅ Testing get_published_drafts...")
            try:
                published = await client.get_published_drafts()
                print(f"✅ Success! Found {len(published)} published drafts")
                
                if published:
                    print("\n📋 First few published drafts:")
                    for i, draft in enumerate(published[:3], 1):
                        print(f"  {i}. ID: {draft.id}")
                        print(f"     First tweet: {draft.text_first_tweet[:60]}...")
                        print(f"     Tweets: {draft.num_tweets}")
                        if draft.published_on:
                            print(f"     Published: {draft.published_on}")
                        if draft.twitter_url:
                            print(f"     Twitter: {draft.twitter_url}")
                        print()
                else:
                    print("📝 No published drafts found")
            except Exception as e:
                print(f"❌ Error getting published drafts: {str(e)}")
            
            print("\n🎉 Read operations test completed!")
            
    except Exception as e:
        print(f"\n❌ Client error: {str(e)}")
        if "403" in str(e):
            print("💡 This might be an API key issue. Please check:")
            print("   - Your API key is correct")
            print("   - Your Typefully account has API access")
        elif "401" in str(e):
            print("💡 Authentication failed. Please check your API key.")


if __name__ == "__main__":
    asyncio.run(test_read_operations()) 