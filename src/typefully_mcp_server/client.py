"""Typefully API client."""

import os
from typing import List, Optional, Dict, Any
import httpx
from .types import Draft, CreateDraftRequest
from .keychain import get_api_key


class TypefullyClient:
    """Client for interacting with the Typefully API."""
    
    BASE_URL = "https://api.typefully.com/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Typefully client.
        
        Args:
            api_key: The Typefully API key. If not provided, will look for:
                     1. TYPEFULLY_API_KEY environment variable
                     2. macOS Keychain (if available)
        """
        self.api_key = api_key or get_api_key()
        if not self.api_key:
            raise ValueError(
                "API key not found. Please either:\n"
                "1. Set TYPEFULLY_API_KEY environment variable, or\n"
                "2. Store in macOS Keychain using Keychain Access app:\n"
                "   - Service: typefully-mcp-server\n"
                "   - Account: api_key\n"
                "   - Password: your_api_key_here"
            )
        
        self.headers = {
            "X-API-KEY": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.client = None
    
    async def __aenter__(self):
        self.client = httpx.AsyncClient(base_url=self.BASE_URL, headers=self.headers)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()
    
    async def create_draft(self, request: CreateDraftRequest) -> Draft:
        """Create a new draft.
        
        Args:
            request: The draft creation request
            
        Returns:
            The created draft
        """
        if not self.client:
            raise RuntimeError("Client not initialized. Use async with statement.")
            
        # Convert the request to dict and handle the schedule-date field
        payload = request.model_dump(exclude_none=True, by_alias=True)
        
        response = await self.client.post("/drafts/", json=payload)
        response.raise_for_status()
        
        return Draft(**response.json())
    
    async def get_scheduled_drafts(self, content_filter: Optional[str] = None) -> List[Draft]:
        """Get recently scheduled drafts.
        
        Args:
            content_filter: Optional filter for "threads" or "tweets"
            
        Returns:
            List of scheduled drafts
        """
        if not self.client:
            raise RuntimeError("Client not initialized. Use async with statement.")
            
        params = {}
        if content_filter:
            params["content_filter"] = content_filter
        
        response = await self.client.get("/drafts/recently-scheduled/", params=params)
        response.raise_for_status()
        
        drafts_data = response.json()
        return [Draft(**draft) for draft in drafts_data]
    
    async def get_published_drafts(self, content_filter: Optional[str] = None) -> List[Draft]:
        """Get recently published drafts.
        
        Args:
            content_filter: Optional filter for "threads" or "tweets"
            
        Returns:
            List of published drafts
        """
        if not self.client:
            raise RuntimeError("Client not initialized. Use async with statement.")
            
        params = {}
        if content_filter:
            params["content_filter"] = content_filter
        
        response = await self.client.get("/drafts/recently-published/", params=params)
        response.raise_for_status()
        
        drafts_data = response.json()
        return [Draft(**draft) for draft in drafts_data] 