# Cursor MCP Setup Guide

This guide will help you configure the Typefully MCP server to work with Cursor.

## 📋 Prerequisites

✅ Typefully MCP server installed (see [README.md](README.md) for installation)
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

### Step 2: Add MCP Server in Cursor Settings

Instead of manually editing config files, use Cursor's built-in MCP settings:

1. **Open Cursor Settings:**
   - Press `Cmd+,` (macOS) or `Ctrl+,` (Windows/Linux)
   - Or go to **Cursor > Settings**

2. **Navigate to MCP Settings:**
   - Search for "MCP" in the settings search bar
   - Or look for **Extensions > MCP** in the settings sidebar

3. **Add Typefully MCP Server:**
   - Click **"Add MCP Server"** or **"+"**
   - Fill in the configuration:
     - **Name**: `typefully`
     - **Command**: `/path/to/your/typefully-mcp-server/venv/bin/python`
     - **Args**: `-m typefully_mcp_server.server`
     - **Working Directory**: `/path/to/your/typefully-mcp-server`
     - **Environment Variables**: (only if using Option B - leave empty for keychain)

4. **Replace paths with your actual project location:**
   ```bash
   # First, get your actual project path:
   cd /path/to/your/typefully-mcp-server
   pwd  # Copy this output for the paths above
   ```

### Step 3: Restart Cursor

After adding the configuration, restart Cursor for the changes to take effect.

## 🧪 Testing the Integration

### Step 4: Verify MCP Server in Cursor

1. Open Cursor
2. Open the command palette (Cmd+Shift+P on macOS)
3. Look for MCP-related commands or check if Typefully tools are available
4. You should see tools like:
   - `create_draft`
   - `get_scheduled_drafts` 
   - `get_published_drafts`

### Step 5: Test with Natural Language

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