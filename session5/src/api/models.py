
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class Meeting(BaseModel):
    title:str
    owner:str
    date:datetime
    content:str

class MeetingRequest(BaseModel):
    title: str
    owner: str

class MeetingResponse(BaseModel):
    id : UUID


    