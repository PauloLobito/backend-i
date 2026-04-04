from dataclasses import dataclass

@dataclass
class Meeting:
    title: str
    owner: str
    date: str


@dataclass
class MeetingMetadata:
    meeting: Meeting
    path: str