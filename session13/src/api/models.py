from datetime import datetime

from pydantic import BaseModel, Field


class ActionItem(BaseModel):
    id: str
    description: str
    owner: str
    due_date: datetime


class Meeting(BaseModel):
    title: str
    owner: str
    participants: list[str] = Field(default_factory=list)
    date: datetime
    status: str = "scheduled"
    content: str = ""
    action_items: list[ActionItem] = Field(default_factory=list)


class MeetingRequest(BaseModel):
    title: str
    owner: str
    due_date: str
    participants: list[str] = Field(default_factory=list)


class MeetingResponse(BaseModel):
    id: str