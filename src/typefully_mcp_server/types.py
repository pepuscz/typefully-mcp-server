"""Type definitions for Typefully API."""

from datetime import datetime
from typing import Optional, Literal, Union
from pydantic import BaseModel, Field


class Draft(BaseModel):
    """Represents a Typefully draft."""
    id: int
    text: Optional[str] = None
    text_first_tweet: str
    num_tweets: int
    scheduled_date: Optional[str] = None
    published_on: Optional[str] = None
    share_url: Optional[str] = None
    twitter_url: Optional[str] = None
    linkedin_url: Optional[str] = None


class CreateDraftRequest(BaseModel):
    """Request model for creating a draft."""
    content: str = Field(..., description="The content of the draft. Use 4 consecutive newlines to split into multiple tweets.")
    threadify: Optional[bool] = Field(False, description="Automatically split content into multiple tweets")
    share: Optional[bool] = Field(False, description="If true, returned payload will include a share_url")
    schedule_date: Optional[Union[str, Literal["next-free-slot"]]] = Field(
        None, 
        alias="schedule-date",
        description="ISO formatted date (e.g.:2022-06-13T11:13:31.662Z) or 'next-free-slot'"
    )
    auto_retweet_enabled: Optional[bool] = Field(False, description="Enable AutoRT for this post")
    auto_plug_enabled: Optional[bool] = Field(False, description="Enable AutoPlug for this post")

    class Config:
        populate_by_name = True


class GetDraftsRequest(BaseModel):
    """Request model for getting drafts."""
    content_filter: Optional[Literal["threads", "tweets"]] = Field(
        None,
        description="Filter drafts to only include tweets or threads"
    ) 