from datetime import datetime

from pydantic import BaseModel


class Meeting(BaseModel):
    title: str
    owner: str
    date: datetime
    content: str


class MeetingRequest(BaseModel):
    title: str
    owner: str
    due_date: str


class MeetingResponse(BaseModel):
    id: str