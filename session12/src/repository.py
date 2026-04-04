import json
from pathlib import Path

from src.api.models import Meeting


class MeetingRepository:
    def __init__(self, file_path: str = "src/meetings.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.file_path.exists():
            self.file_path.write_text("{}", encoding="utf-8")

    def _read(self) -> dict[str, dict]:
        with self.file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _write(self, data: dict[str, dict]) -> None:
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def list_all(self) -> dict[str, Meeting]:
        data = self._read()
        return {
            meeting_id: Meeting(**meeting_data)
            for meeting_id, meeting_data in data.items()
        }

    def save(self, meeting_id: str, meeting: Meeting) -> None:
        data = self._read()
        data[meeting_id] = meeting.model_dump(mode="json")
        self._write(data)

    def get(self, meeting_id: str) -> Meeting | None:
        data = self._read()
        meeting_data = data.get(meeting_id)

        if meeting_data is None:
            return None

        return Meeting(**meeting_data)

    def delete(self, meeting_id: str) -> bool:
        data = self._read()

        if meeting_id not in data:
            return False

        del data[meeting_id]
        self._write(data)
        return True