# Cursor MCP Setup Guide

This guide will help you configure the Typefully MCP server to work with Cursor.

## 📋 Prerequisites

✅ Typefully MCP server installed and tested
✅ Cursor installed
✅ Typefully API key (get it from Settings > Integrations in Typefully)

## 🔧 Configuration Steps

### Step 1: Configure API Key Storage

You have two options for storing your Typefully API key:

#### Option A: macOS Keychain (Recommended) 🔐

1. **Add your API key to Keychain Access:**
   - Open **Keychain Access** app (Applications > Utilities)
   - **Important**: Make sure you're adding to the **System** keychain (not iCloud keychain)
   - Click **File > New Password Item**
   - Set **Keychain Item Name**: `typefully-mcp-server`
   - Set **Account Name**: `api_key`
   - Set **Password**: `your_actual_api_key_here`
   - **Keychain**: Select **System** (not iCloud)
   - Click **Add**

2. **Configure Access Control:**
   - Double-click the newly created keychain entry
   - Go to the **Access Control** tab
   - Choose **"Allow access by all applications"** for simplest setup
   - Click **Save Changes**

#### Option B: Environment Variables

You can include the API key directly in the Cursor configuration (less secure but simpler).

### Step 2: Locate Cursor Configuration Directory

The MCP configuration location depends on your operating system:

- **macOS**: `~/Library/Application Support/Cursor/User/globalStorage/mcp-config.json`
- **Windows**: `%APPDATA%\Cursor\User\globalStorage\mcp-config.json`  
- **Linux**: `~/.config/Cursor/User/globalStorage/mcp-config.json`

**Note**: These paths are for newer versions of Cursor. If the file doesn't exist, create the directory structure first.

### Step 3: Create or Update MCP Configuration

If the file doesn't exist, create it. If it exists, add our server configuration to the existing `mcpServers` object.

#### If using Keychain (Option A):

```json
{
  "mcpServers": {
    "typefully": {
      "command": "/path/to/your/typefully-mcp-server/venv/bin/python",
      "args": ["-m", "typefully_mcp_server.server"],
      "cwd": "/path/to/your/typefully-mcp-server"
    }
  }
}
```

#### If using Environment Variables (Option B):

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

**Important**: Replace `/path/to/your/typefully-mcp-server/` with your actual project path.

### Step 4: Quick Setup Commands

Run these commands to set up the configuration:

```bash
# Navigate to project directory
cd /path/to/your/typefully-mcp-server

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (including keyring for macOS Keychain support)
pip install -e .

# Create Cursor config directory if it doesn't exist (macOS)
mkdir -p ~/Library/Application\ Support/Cursor/User/globalStorage

# Create the MCP configuration file
# Edit the file with your actual project path
```

### Step 5: Restart Cursor

After adding the configuration, restart Cursor for the changes to take effect.

## 🧪 Testing the Integration

### Step 6: Verify MCP Server in Cursor

1. Open Cursor
2. Open the command palette (Cmd+Shift+P on macOS)
3. Look for MCP-related commands or check if Typefully tools are available
4. You should see tools like:
   - `create_draft`
   - `get_scheduled_drafts` 
   - `get_published_drafts`

### Step 7: Test with Natural Language

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
- Test the server manually: `source venv/bin/activate && python test_read_api.py`

**4. Server not starting**
- Check the logs in Cursor
- Test server directly: `source venv/bin/activate && python -m typefully_mcp_server.server`

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