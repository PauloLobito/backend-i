from src.main import cli
from src.services import meeting

@cli.command()
def create(
    title = str,
    owner = str,
    date =str
) -> None:
    meeting.create(title,owner,date)