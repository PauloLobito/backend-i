from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    detail: str


class ValidationErrorResponse(BaseModel):
    detail: str
    errors: list[dict]


class MeetingCreate(BaseModel):
    title: str = Field(min_length=3)
    date: str
    owner: str = Field(min_length=2)
    participants: list[str] = Field(min_length=1)


class MeetingRead(BaseModel):
    id: str
    title: str
    date: str
    owner: str
    participants: list[str]
    content: str = ""
    action_items: list[str] = Field(default_factory=list)