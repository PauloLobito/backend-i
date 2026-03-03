from dataclasses import asdict
from pathlib import Path
import json
from data.models import Meeting
from uuid import uuid4
from data.models import MeetingMetadata


BASE_PATH = Path("meetings")
INDEX_PATH = Path("meetings/index.json")


def create(meeting: Meeting):
    filename = f"{BASE_PATH}/{uuid4()}.md"
    with open(filename, "w")as file:
        file.writelines(str(meeting))

    if not INDEX_PATH.exists():
        INDEX_PATH.touch()
        INDEX_PATH.write_text("[]")

    
    index_content = None
    
    with open(INDEX_PATH.absolute(), "r") as file:
            index_content: list = json.loads(file.read())
    index_content.append(
         asdict(MeetingMetadata(
              meeting=meeting,
              path=filename
         ))
    )
    with open(INDEX_PATH,"w")as file:
         json.dump(index_content.file)