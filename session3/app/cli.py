import typer

from app.services.meeting_service import (
    create_meeting,
    list_meetings,
    get_meeting_by_id,
)

app = typer.Typer()


@app.command("create-meeting")
def create_meeting_cmd(title: str, date: str, owner: str) -> None:
    meeting = create_meeting(title, date, owner)
    typer.echo(f"Created: {meeting.id}")


@app.command("list-meetings")
def list_meetings_cmd() -> None:
    for m in list_meetings():
        typer.echo(f"{m.id} | {m.date} | {m.title}")


@app.command("show-meeting")
def show_meeting_cmd(id: str) -> None:
    meeting = get_meeting_by_id(id)

    if not meeting:
        typer.echo("Meeting not found")
        raise typer.Exit(code=1)

    typer.echo(f"{meeting.id} | {meeting.date} | {meeting.title}")