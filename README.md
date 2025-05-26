# Typefully MCP Server

A Model Context Protocol (MCP) server that provides integration with the Typefully API, allowing AI assistants to create and manage drafts on Typefully.

## Features

- **Create drafts** with full support for:
  - Multi-tweet threads (using 4 newlines as separator)
  - Automatic threadification
  - Scheduling (specific date/time or next free slot)
  - AutoRT and AutoPlug features
  - Share URLs
- **Get scheduled drafts** with optional filtering
- **Get published drafts** with optional filtering

## Installation

### Prerequisites

- Python 3.10 or higher
- A Typefully account with API access
- Your Typefully API key (get it from Settings > Integrations in Typefully)

### Install from source

1. Clone this repository:
```bash
git clone <repository-url>
cd typefully-mcp-server
```

2. Install the package:
```bash
pip install -e .
```

Or using requirements.txt:
```bash
pip install -r requirements.txt
```

## Configuration

### API Key Management

This server supports secure API key storage using macOS Keychain. You have two options:

#### Option 1: macOS Keychain (Recommended) 🔐

Store your API key securely using the **Keychain Access** app:

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
   - Or add specific Python executable: `/opt/homebrew/opt/python@3.13/bin/python3.13`
   - Click **Save Changes**

**Important Notes:**
- ⚠️ **Must use System keychain** - iCloud keychain won't work with the MCP server
- ⚠️ **Access control required** - You'll need to allow Python applications to access the key
- 🔒 **Security consideration** - "Allow all applications" lets any Python script access this key



#### Option 2: Environment Variables

You can set the API key as an environment variable or include it directly in your MCP configuration.

**Note:** Environment variables take priority over keychain storage for compatibility.

### MCP Configuration

Add the server to your MCP configuration file. **With keychain storage, you don't need to include the API key in the config:**

```json
{
  "mcpServers": {
    "typefully": {
      "command": "python",
      "args": ["-m", "typefully_mcp_server.server"]
    }
  }
}
```

If using environment variables, include the key:

```json
{
  "mcpServers": {
    "typefully": {
      "command": "python",
      "args": ["-m", "typefully_mcp_server.server"],
      "env": {
        "TYPEFULLY_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Usage

Once configured, the MCP server provides the following tools:

### create_draft

Create a new draft in Typefully.

**Parameters:**
- `content` (required): The content of the draft. Use 4 consecutive newlines to split into multiple tweets.
- `threadify` (optional): Automatically split content into multiple tweets
- `share` (optional): If true, returned payload will include a share_url
- `schedule_date` (optional): ISO formatted date (e.g., "2024-01-15T10:30:00Z") or "next-free-slot"
- `auto_retweet_enabled` (optional): Enable AutoRT for this post
- `auto_plug_enabled` (optional): Enable AutoPlug for this post

**Example:**
```
Create a draft with content "Hello from MCP! This is my first automated tweet." and schedule it for next free slot
```

### get_scheduled_drafts

Get recently scheduled drafts from Typefully.

**Parameters:**
- `content_filter` (optional): Filter drafts to only include "tweets" or "threads"

**Example:**
```
Get my scheduled drafts that are threads only
```

### get_published_drafts

Get recently published drafts from Typefully.

**Parameters:**
- `content_filter` (optional): Filter drafts to only include "tweets" or "threads"

**Example:**
```
Show me all my recently published tweets
```

## Testing

A test script is included to verify the server functionality:

```bash
# Test the API connectivity (requires API key configured)
python test_read_api.py
```

## Development

### Project Structure

```
typefully-mcp-server/
├── src/
│   └── typefully_mcp_server/
│       ├── __init__.py
│       ├── server.py      # Main MCP server implementation
│       ├── client.py      # Typefully API client
│       ├── keychain.py    # Secure keychain integration
│       └── types.py       # Type definitions
├── pyproject.toml
├── requirements.txt
├── README.md
└── test_read_api.py       # Test script
```

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## API Reference

This MCP server implements a subset of the [Typefully API](https://support.typefully.com/en/articles/8718287-typefully-api). For more details on the API endpoints and options, refer to the official documentation.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 