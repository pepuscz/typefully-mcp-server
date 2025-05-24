#!/usr/bin/env python3
"""Test script for MCP server tools."""

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

from typefully_mcp_server.server import app


async def test_mcp_tools():
    """Test MCP server tools directly."""
    print("🔧 Testing MCP Server Tools")
    print("=" * 50)
    
    # Set environment variable for testing
    os.environ["TYPEFULLY_API_KEY"] = "1pfoHORJ6dQZ985w"
    
    # Import the call_tool handler function 
    from typefully_mcp_server.server import call_tool
    
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