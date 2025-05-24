"""MCP server for Typefully API integration."""

import asyncio
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.lowlevel import NotificationOptions
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
from pydantic import AnyUrl

from .client import TypefullyClient
from .types import CreateDraftRequest, Draft

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the MCP server instance
app = Server("typefully-mcp-server")


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools for Typefully integration."""
    return [
        Tool(
            name="create_draft",
            description="Create a new draft in Typefully with optional scheduling",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The content of the draft. Use 4 consecutive newlines to split into multiple tweets."
                    },
                    "threadify": {
                        "type": "boolean",
                        "description": "Automatically split content into multiple tweets",
                        "default": False
                    },
                    "share": {
                        "type": "boolean",
                        "description": "If true, returned payload will include a share_url",
                        "default": False
                    },
                    "schedule_date": {
                        "type": "string",
                        "description": "ISO formatted date (e.g.:2022-06-13T11:13:31.662Z) or 'next-free-slot'",
                        "oneOf": [
                            {"type": "string", "format": "date-time"},
                            {"type": "string", "enum": ["next-free-slot"]}
                        ]
                    },
                    "auto_retweet_enabled": {
                        "type": "boolean",
                        "description": "Enable AutoRT for this post",
                        "default": False
                    },
                    "auto_plug_enabled": {
                        "type": "boolean",
                        "description": "Enable AutoPlug for this post",
                        "default": False
                    }
                },
                "required": ["content"]
            }
        ),
        Tool(
            name="get_scheduled_drafts",
            description="Get recently scheduled drafts from Typefully",
            inputSchema={
                "type": "object",
                "properties": {
                    "content_filter": {
                        "type": "string",
                        "description": "Filter drafts to only include tweets or threads",
                        "enum": ["threads", "tweets"]
                    }
                }
            }
        ),
        Tool(
            name="get_published_drafts",
            description="Get recently published drafts from Typefully",
            inputSchema={
                "type": "object",
                "properties": {
                    "content_filter": {
                        "type": "string",
                        "description": "Filter drafts to only include tweets or threads",
                        "enum": ["threads", "tweets"]
                    }
                }
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls for Typefully operations."""
    try:
        async with TypefullyClient() as client:
            if name == "create_draft":
                # Create the draft request
                request = CreateDraftRequest(**arguments)
                draft = await client.create_draft(request)
                
                # Format the response
                result = f"✅ Draft created successfully!\n\n"
                result += f"**Draft ID:** {draft.id}\n"
                result += f"**First tweet:** {draft.text_first_tweet[:100]}...\n" if len(draft.text_first_tweet) > 100 else f"**First tweet:** {draft.text_first_tweet}\n"
                result += f"**Number of tweets:** {draft.num_tweets}\n"
                
                if draft.scheduled_date:
                    result += f"**Scheduled for:** {draft.scheduled_date}\n"
                
                if draft.share_url:
                    result += f"**Share URL:** {draft.share_url}\n"
                
                result += f"\n**View draft:** https://typefully.com/?d={draft.id}"
                
                return [TextContent(type="text", text=result)]
            
            elif name == "get_scheduled_drafts":
                content_filter = arguments.get("content_filter")
                drafts = await client.get_scheduled_drafts(content_filter)
                
                if not drafts:
                    return [TextContent(type="text", text="No scheduled drafts found.")]
                
                result = f"📅 Found {len(drafts)} scheduled draft(s):\n\n"
                
                for i, draft in enumerate(drafts, 1):
                    result += f"**{i}. Draft ID {draft.id}**\n"
                    result += f"   First tweet: {draft.text_first_tweet[:80]}...\n" if len(draft.text_first_tweet) > 80 else f"   First tweet: {draft.text_first_tweet}\n"
                    result += f"   Tweets: {draft.num_tweets}\n"
                    if draft.scheduled_date:
                        result += f"   Scheduled: {draft.scheduled_date}\n"
                    result += f"   View: https://typefully.com/?d={draft.id}\n\n"
                
                return [TextContent(type="text", text=result)]
            
            elif name == "get_published_drafts":
                content_filter = arguments.get("content_filter")
                drafts = await client.get_published_drafts(content_filter)
                
                if not drafts:
                    return [TextContent(type="text", text="No published drafts found.")]
                
                result = f"✅ Found {len(drafts)} published draft(s):\n\n"
                
                for i, draft in enumerate(drafts, 1):
                    result += f"**{i}. Draft ID {draft.id}**\n"
                    result += f"   First tweet: {draft.text_first_tweet[:80]}...\n" if len(draft.text_first_tweet) > 80 else f"   First tweet: {draft.text_first_tweet}\n"
                    result += f"   Tweets: {draft.num_tweets}\n"
                    if draft.published_on:
                        result += f"   Published: {draft.published_on}\n"
                    if draft.twitter_url:
                        result += f"   Twitter: {draft.twitter_url}\n"
                    if draft.linkedin_url:
                        result += f"   LinkedIn: {draft.linkedin_url}\n"
                    result += "\n"
                
                return [TextContent(type="text", text=result)]
            
            else:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]
                
    except Exception as e:
        logger.error(f"Error calling tool {name}: {str(e)}")
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="typefully-mcp-server",
                    server_version="0.1.0",
                    capabilities=app.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
    
    asyncio.run(main()) 