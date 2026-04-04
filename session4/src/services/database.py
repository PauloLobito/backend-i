from dataclasses import asdict
from pathlib import Path
import json
from uuid import uuid4

from src.data.models import Meeting, MeetingMetadata

BASE_PATH = Path("meetings")
INDEX_PATH = BASE_PATH / "index.json"


def create(meeting: Meeting) -> None:
    BASE_PATH.mkdir(parents=True, exist_ok=True)

    filename = BASE_PATH / f"{uuid4()}.md"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(meeting))

    if not INDEX_PATH.exists():
        INDEX_PATH.write_text("[]", encoding="utf-8")

    raw_content = INDEX_PATH.read_text(encoding="utf-8").strip()

    if not raw_content:
        index_content = []
    else:
        index_content = json.loads(raw_content)

    index_content.append(
        asdict(
            MeetingMetadata(
                meeting=meeting,
                path=str(filename),
            )
        )
    )

    with open(INDEX_PATH, "w", encoding="utf-8") as file:
        json.dump(index_content, file, indent=2, ensure_ascii=False)