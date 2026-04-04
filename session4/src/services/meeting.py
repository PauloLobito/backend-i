from src.data.models import Meeting
from src.services import database



def create(title:str,owner:str,date:str)-> None:
    new_meeting = Meeting(
        title=title,
        owner=owner,
        date=date
    )
    database.create(meeting = new_meeting)

def list():
    ...
