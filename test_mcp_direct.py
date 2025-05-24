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
    os.environ["TYPEFULLY_API_KEY"] = "1pfoHORJ6dQZ985w"
    
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