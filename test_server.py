#!/usr/bin/env python3
"""Test script for Typefully MCP server."""

import asyncio
import os
from dotenv import load_dotenv
from src.typefully_mcp_server.client import TypefullyClient
from src.typefully_mcp_server.types import CreateDraftRequest

# Load environment variables
load_dotenv()


async def test_client():
    """Test the Typefully client directly."""
    print("Testing Typefully MCP Server Client...")
    print("=" * 50)
    
    # Check for API key
    api_key = os.getenv("TYPEFULLY_API_KEY")
    if not api_key:
        print("❌ Error: TYPEFULLY_API_KEY not found in environment variables")
        print("Please create a .env file with your API key")
        return
    
    print("✅ API key found")
    
    try:
        async with TypefullyClient() as client:
            # Test 1: Get scheduled drafts
            print("\n📅 Testing get_scheduled_drafts...")
            scheduled = await client.get_scheduled_drafts()
            print(f"Found {len(scheduled)} scheduled drafts")
            
            # Test 2: Get published drafts
            print("\n✅ Testing get_published_drafts...")
            published = await client.get_published_drafts()
            print(f"Found {len(published)} published drafts")
            
            # Test 3: Create a test draft (commented out by default)
            print("\n📝 Create draft test (uncomment to test):")
            print("# Uncomment the following lines to test draft creation:")
            print("# request = CreateDraftRequest(")
            print('#     content="Test draft from MCP server! 🚀",')
            print("#     threadify=False,")
            print("#     share=True")
            print("# )")
            print("# draft = await client.create_draft(request)")
            print('# print(f"Created draft with ID: {draft.id}")')
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("Typefully MCP Server Test")
    print("=" * 50)
    asyncio.run(test_client()) 