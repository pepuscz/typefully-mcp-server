#!/usr/bin/env python3
"""Test script for MCP server tools."""

import asyncio
import os
from dotenv import load_dotenv
from src.typefully_mcp_server.server import call_tool

# Load environment variables
load_dotenv()


async def test_mcp_tools():
    """Test MCP server tools directly."""
    print("🔧 Testing MCP Server Tools")
    print("=" * 50)
    
    # Test get_scheduled_drafts tool
    print("\n📅 Testing get_scheduled_drafts tool...")
    try:
        result = await call_tool("get_scheduled_drafts", {})
        print("✅ Success!")
        print("Response:", result[0].text)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test get_published_drafts tool
    print("\n✅ Testing get_published_drafts tool...")
    try:
        result = await call_tool("get_published_drafts", {})
        print("✅ Success!")
        print("Response preview:", result[0].text[:200] + "..." if len(result[0].text) > 200 else result[0].text)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test get_published_drafts with filter
    print("\n🔍 Testing get_published_drafts with filter (threads only)...")
    try:
        result = await call_tool("get_published_drafts", {"content_filter": "threads"})
        print("✅ Success!")
        print("Response preview:", result[0].text[:200] + "..." if len(result[0].text) > 200 else result[0].text)
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(test_mcp_tools()) 