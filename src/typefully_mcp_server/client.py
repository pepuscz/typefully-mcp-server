"""Typefully API client."""

import os
from typing import List, Optional, Dict, Any
import httpx
from .types import Draft, CreateDraftRequest


class TypefullyClient:
    """Client for interacting with the Typefully API."""
    
    BASE_URL = "https://api.typefully.com/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Typefully client.
        
        Args:
            api_key: The Typefully API key. If not provided, will look for TYPEFULLY_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("TYPEFULLY_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set in TYPEFULLY_API_KEY environment variable")
        
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