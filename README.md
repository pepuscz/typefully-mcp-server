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

### Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd typefully-mcp-server
```

2. Create virtual environment and install:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

## Configuration

### Environment Variables

Create a `.env` file in your project root (you can copy from `env.example`):

```bash
cp env.example .env
# Edit .env and add your API key
```

### MCP Configuration

Add the server to your MCP configuration file:

**For Claude Desktop:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

**For Cursor:**
- macOS: `~/Library/Application Support/Cursor/User/globalStorage/mcp-config.json`
- Windows: `%APPDATA%\Cursor\User\globalStorage\mcp-config.json`
- Linux: `~/.config/Cursor/User/globalStorage/mcp-config.json`

```json
{
  "mcpServers": {
    "typefully": {
      "command": "/absolute/path/to/your/venv/bin/python",
      "args": ["-m", "typefully_mcp_server.server"],
      "env": {
        "TYPEFULLY_API_KEY": "your_api_key_here"
      },
      "cwd": "/absolute/path/to/typefully-mcp-server"
    }
  }
}
```

**Important**: Use absolute paths for both the Python executable and working directory for better reliability.

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

Several test scripts are included to verify the server functionality:

```bash
# Test basic server functionality
python test_read_api.py

# Test MCP tools directly  
python test_mcp_tools.py

# Test server startup and tool registration
python test_mcp_direct.py
```

You can also test the server directly:

```bash
# Activate your virtual environment
source venv/bin/activate

# Test server startup
python -m typefully_mcp_server.server
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
│       └── types.py       # Type definitions
├── pyproject.toml
├── requirements.txt
├── README.md
├── env.example
├── test_read_api.py       # API functionality tests
├── test_mcp_tools.py      # MCP tools tests
└── test_mcp_direct.py     # Server startup tests
```

### Recent Updates

This project has been updated to use the latest MCP Python SDK (v1.9+) with proper:
- Server initialization with `NotificationOptions`
- Import path fixes for development and testing
- Compatibility with current Cursor and Claude Desktop versions

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