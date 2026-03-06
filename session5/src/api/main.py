from datetime import datetime

from fastapi import FastAPI

from api.models import Meeting, MeetingRequest, MeetingResponse


api = FastAPI()

# @api.get("/shop")
# def list_products():
#      ...

# @api.get("/shop/{category}")
# def list2_products(category:str):
#      return f"Category - {category}"

# @api.get("/shop/{products}")
# def list3_products(products:str):
#      return f"Products - {products}"

# @api.post("/shop")
# def list4_products():
#      ...

@api.get("/",response_model=list[Meeting])
def list_meetings(title:str = "",owner:str = "",date:datetime| None = None)->list[Meeting]:
     return []

@api.post("/", response_model=MeetingResponse)
def create_meetings(meeting:MeetingRequest):
     ...

@api.get("/{meeting_id}",response_model=Meeting)
def get_meeting(meeting_id:str):
     ...