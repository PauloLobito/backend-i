from datetime import datetime

from pydantic import BaseModel, Field


class Meeting(BaseModel):
    title: str
    owner: str
    participants: list[str] = Field(default_factory=list)
    date: datetime
    content: str = ""
    action_items: list[str] = Field(default_factory=list)


class MeetingRequest(BaseModel):
    title: str
    owner: str
    due_date: str
    participants: list[str] = Field(default_factory=list)


class MeetingResponse(BaseModel):
    id: str