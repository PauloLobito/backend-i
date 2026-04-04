from datetime import datetime

from pydantic import BaseModel, Field


class Meeting(BaseModel):
    title: str
    owner: str
    date: datetime
    content: str = ""
    action_items: list[str] = Field(default_factory=list)


class MeetingRequest(BaseModel):
    title: str
    owner: str
    due_date: str


class MeetingResponse(BaseModel):
    id: str