#!/usr/bin/env python3
"""Verify Cursor MCP setup for Typefully."""

import json
import os
from pathlib import Path

def verify_cursor_setup():
    """Verify that Cursor MCP configuration is set up correctly."""
    print("🔍 Verifying Cursor MCP Setup")
    print("=" * 50)
    
    # Check configuration file
    config_path = Path.home() / "Library/Application Support/Cursor/User/globalStorage/mcp-config.json"
    
    print(f"📁 Checking config file: {config_path}")
    
    if not config_path.exists():
        print("❌ Configuration file not found!")
        print(f"   Expected location: {config_path}")
        return False
    
    print("✅ Configuration file exists")
    
    # Read and validate configuration
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        print("✅ Configuration file is valid JSON")
        
        # Check for our server
        if 'mcpServers' not in config:
            print("❌ No mcpServers section found")
            return False
        
        if 'typefully' not in config['mcpServers']:
            print("❌ Typefully server not configured")
            return False
        
        typefully_config = config['mcpServers']['typefully']
        print("✅ Typefully server configuration found")
        
        # Verify configuration details
        required_fields = ['command', 'args', 'env', 'cwd']
        for field in required_fields:
            if field in typefully_config:
                if field == 'env' and 'TYPEFULLY_API_KEY' in typefully_config[field]:
                    api_key = typefully_config[field]['TYPEFULLY_API_KEY']
                    if api_key and api_key != 'your_typefully_api_key_here':
                        print(f"✅ {field}: API key configured")
                    else:
                        print(f"❌ {field}: API key not properly set")
                else:
                    print(f"✅ {field}: {typefully_config[field]}")
            else:
                print(f"❌ Missing {field}")
                return False
        
        # Check Python executable
        python_path = typefully_config['command']
        if os.path.exists(python_path):
            print(f"✅ Python executable exists: {python_path}")
        else:
            print(f"❌ Python executable not found: {python_path}")
            return False
        
        # Check working directory
        cwd = typefully_config['cwd']
        if os.path.exists(cwd):
            print(f"✅ Working directory exists: {cwd}")
        else:
            print(f"❌ Working directory not found: {cwd}")
            return False
        
        # Check API key
        api_key = typefully_config['env'].get('TYPEFULLY_API_KEY')
        if api_key and api_key != 'your_typefully_api_key_here':
            print("✅ API key configured properly")
        else:
            print("❌ API key not properly configured")
            return False
        
        print("\n🎉 Configuration verification completed successfully!")
        print("\n📋 Next steps:")
        print("1. Restart Cursor if it's currently running")
        print("2. Open Cursor and check if MCP tools are available")
        print("3. Try asking: 'Show me my Typefully drafts'")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in configuration file: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading configuration: {e}")
        return False

if __name__ == "__main__":
    success = verify_cursor_setup()
    exit(0 if success else 1) 