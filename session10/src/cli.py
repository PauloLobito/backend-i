import json
import logging

import typer
from typer import Typer

from src.core.logging_config import configure_logging
from src.core.errors import NotFoundError, ValidationError
from src.report_service import period_summary, summary
from src.repository import MeetingRepository
from src.services import MeetingService

configure_logging()
logger = logging.getLogger(__name__)

app = Typer(
    name="FASTAPI CLI",
)

ERROR_CODES = {
    ValidationError: 2,
    NotFoundError: 3,
}

repository = MeetingRepository()
service = MeetingService(repository)


def handle_error(exc: Exception) -> None:
    code = ERROR_CODES.get(type(exc), 1)
    typer.echo(f"Erro: {exc}")
    raise typer.Exit(code=code)


@app.command()
def run():
    import uvicorn
    from src.api.main import app as fastapi_app

    logger.info("Starting API server")
    uvicorn.run(fastapi_app, host="127.0.0.1", port=8000, reload=True)


@app.command("create-meeting")
def create_meeting(
    title: str = typer.Option(..., "--title"),
    date: str = typer.Option(..., "--date"),
    owner: str = typer.Option(..., "--owner"),
):
    try:
        meeting = service.create_meeting(
            title=title,
            owner=owner,
            due_date=date,
        )
        typer.echo(f"Meeting criada com id={meeting.id}")
    except (ValidationError, NotFoundError) as exc:
        handle_error(exc)


@app.command("list-meetings")
def list_meetings():
    meetings = service.list_meetings()

    if not meetings:
        typer.echo("Nenhuma meeting encontrada")
        return

    for meeting_id, meeting in meetings.items():
        typer.echo(
            f"{meeting_id} | {meeting.title} | {meeting.owner} | "
            f"{meeting.date.strftime('%Y-%m-%d')}"
        )


@app.command("show-meeting")
def show_meeting(
    id: str = typer.Option(..., "--id"),
):
    try:
        meeting = service.show_meeting(id)
        typer.echo(
            json.dumps(
                meeting.model_dump(mode="json"),
                indent=2,
                ensure_ascii=False,
            )
        )
    except (ValidationError, NotFoundError) as exc:
        handle_error(exc)


@app.command("delete-meeting")
def delete_meeting(
    id: str = typer.Option(..., "--id"),
):
    try:
        service.delete_meeting(id)
        typer.echo(f"Meeting removida: {id}")
    except (ValidationError, NotFoundError) as exc:
        handle_error(exc)


@app.command("summary")
def summary_command():
    try:
        meetings = list(service.list_meetings().values())
        typer.echo(json.dumps(summary(meetings), indent=2, ensure_ascii=False))
    except (ValidationError, NotFoundError) as exc:
        handle_error(exc)


@app.command("period-report")
def period_report(
    from_date: str = typer.Option(..., "--from-date"),
    to_date: str = typer.Option(..., "--to-date"),
):
    try:
        meetings = list(service.list_meetings().values())
        report = period_summary(meetings, from_date, to_date)
        typer.echo(json.dumps(report, indent=2, ensure_ascii=False))
    except (ValidationError, NotFoundError) as exc:
        handle_error(exc)


if __name__ == "__main__":
    app()