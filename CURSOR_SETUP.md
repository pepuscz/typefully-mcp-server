# Cursor MCP Setup Guide

This guide will help you configure the Typefully MCP server to work with Cursor.

## 📋 Prerequisites

✅ Typefully MCP server installed and tested
✅ Cursor installed
✅ Typefully API key configured

## 🔧 Configuration Steps

### Step 1: Locate Cursor Configuration Directory

The MCP configuration location depends on your operating system:

- **macOS**: `~/Library/Application Support/Cursor/User/globalStorage/mcp-config.json`
- **Windows**: `%APPDATA%\Cursor\User\globalStorage\mcp-config.json`  
- **Linux**: `~/.config/Cursor/User/globalStorage/mcp-config.json`

**Note**: These paths are for newer versions of Cursor. If the file doesn't exist, create the directory structure first.

### Step 2: Create or Update MCP Configuration

If the file doesn't exist, create it. If it exists, add our server configuration to the existing `mcpServers` object.

Copy the contents from `cursor-mcp-config.example.json` and update the paths:

```json
{
  "mcpServers": {
    "typefully": {
      "command": "/path/to/your/typefully-mcp-server/venv/bin/python",
      "args": ["-m", "typefully_mcp_server.server"],
      "env": {
        "TYPEFULLY_API_KEY": "your_typefully_api_key_here"
      },
      "cwd": "/path/to/your/typefully-mcp-server"
    }
  }
}
```

**Important**: Replace the following placeholders:
- `/path/to/your/typefully-mcp-server/` with your actual project path
- `your_typefully_api_key_here` with your actual Typefully API key

### Step 3: Quick Setup Commands

Run these commands to set up the configuration (update paths as needed):

```bash
# Navigate to project directory
cd /path/to/your/typefully-mcp-server

# Create virtual environment if not exists
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .

# Create Cursor config directory if it doesn't exist (macOS/Linux)
mkdir -p ~/Library/Application\ Support/Cursor/User/globalStorage

# Copy and customize the example configuration
cp cursor-mcp-config.example.json ~/Library/Application\ Support/Cursor/User/globalStorage/mcp-config.json
# Edit the file to update the absolute paths and API key
```

### Step 4: Restart Cursor

After adding the configuration, restart Cursor for the changes to take effect.

## 🧪 Testing the Integration

### Step 5: Verify MCP Server in Cursor

1. Open Cursor
2. Open the command palette (Cmd+Shift+P on macOS)
3. Look for MCP-related commands or check if Typefully tools are available
4. You should see tools like:
   - `create_draft`
   - `get_scheduled_drafts` 
   - `get_published_drafts`

### Step 6: Test with Natural Language

Try asking Cursor to:

```
"Show me my recent Typefully drafts"
"Get my scheduled posts from Typefully"
"Create a new draft on Typefully with the content: 'Testing MCP integration! 🚀'"
```

## 🔍 Troubleshooting

### Common Issues:

**1. Command not found**
- Make sure the Python path is correct
- Verify the virtual environment exists

**2. Permission denied**
- Check file permissions on the configuration
- Ensure Cursor can access the project directory

**3. API errors**
- Verify your API key is correct
- Test the server manually: `python test_mcp_tools.py`

**4. Server not starting**
- Check the logs in Cursor
- Test server directly: `python -m typefully_mcp_server.server`

### Manual Configuration Check:

```bash
# Test if the server starts correctly
cd /path/to/your/typefully-mcp-server
source venv/bin/activate
python -m typefully_mcp_server.server
```

## 📱 Available Tools

Once configured, you'll have access to these Typefully tools in Cursor:

### `create_draft`
- **Purpose**: Create new drafts with scheduling options
- **Example**: "Create a draft about AI developments"

### `get_scheduled_drafts` 
- **Purpose**: View your scheduled posts
- **Example**: "Show me what I have scheduled"

### `get_published_drafts`
- **Purpose**: View your published content
- **Example**: "What have I published recently?"

## 🎉 You're Ready!

Your Cursor is now connected to Typefully! You can create and manage your social media content directly from your code editor.

---

**Need help?** Check the main README.md or run the test scripts to verify everything is working. 