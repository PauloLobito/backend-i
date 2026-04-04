from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    detail: str


class ValidationErrorResponse(BaseModel):
    detail: str
    errors: list[dict]


class ActionItemCreate(BaseModel):
    description: str = Field(min_length=3)
    owner: str = Field(min_length=2)
    due_date: str


class ActionItemRead(ActionItemCreate):
    id: str


class MeetingCreate(BaseModel):
    title: str = Field(min_length=3)
    date: str
    owner: str = Field(min_length=2)
    participants: list[str] = Field(min_length=1)


class MeetingUpdate(BaseModel):
    title: str = Field(min_length=3)
    date: str
    owner: str = Field(min_length=2)
    participants: list[str] = Field(min_length=1)
    content: str = ""
    action_items: list[ActionItemRead] = Field(default_factory=list)


class MeetingStatusUpdate(BaseModel):
    status: str


class MeetingRead(BaseModel):
    id: str
    title: str
    date: str
    owner: str
    participants: list[str]
    status: str
    content: str = ""
    action_items: list[ActionItemRead] = Field(default_factory=list)