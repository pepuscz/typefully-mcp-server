#!/usr/bin/env python3
"""Direct test of MCP server functionality."""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from typefully_mcp_server.server import create_server

async def test_server():
    """Test if the server starts and lists tools."""
    print("🧪 Testing MCP Server Direct Startup")
    print("=" * 50)
    
    # Set environment variable
    api_key = os.getenv("TYPEFULLY_API_KEY")
    if not api_key:
        print("❌ TYPEFULLY_API_KEY environment variable not set")
        print("Please set it with one of these methods:")
        print("  1. export TYPEFULLY_API_KEY=your_api_key_here")
        print("  2. Create a .env file with: TYPEFULLY_API_KEY=your_api_key_here")
        print("  3. Copy env.example to .env and edit it")
        print("\n💡 Get your API key from Typefully Settings > Integrations")
        return False
    
    try:
        # Create server instance
        server = create_server()
        
        # Get tools list
        tools = server._tool_registry._tools
        
        print(f"✅ Server created successfully")
        print(f"✅ Number of tools registered: {len(tools)}")
        
        for tool_name in tools.keys():
            print(f"  📌 Tool: {tool_name}")
        
        print("\n🎉 MCP Server is working correctly!")
        print("The issue might be with Cursor's connection to the server.")
        print("\n💡 Try:")
        print("1. Restart Cursor completely")
        print("2. Check Cursor's logs for MCP errors")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating server: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_server())
    sys.exit(0 if success else 1) 