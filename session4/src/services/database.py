from pathlib import Path
import json
from data.models import Meeting
from uuid import uuid4


BASE_PATH = Path("meetings")
INDEX_PATH = Path("meetings/index.json")


def create(meeting: Meeting):
    filename = f"{BASE_PATH}/{uuid4()}.md"
    with open(filename, "w")as file:
        file.writelines(str(meeting))

    if not INDEX_PATH.exists():
        INDEX_PATH.touch()

    breakpoint()
    index_content = None
    with open(INDEX_PATH.absolute(), "r") as file:
        index_content = json.loads(file.read())
