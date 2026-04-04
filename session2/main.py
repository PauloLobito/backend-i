import typer

from app.domain.models import Meeting, ActionItem
from app.services.meeting_service import add_meeting, list_meetings

app = typer.Typer()


@app.command()
def seed():
    meeting = Meeting(
        id="m1",
        title="Sprint Planning",
        date="2026-03-10",
        owner="Ana",
        participants=["Ana", "Carlos", "João"],
        action_items=[
            ActionItem(
                description="Preparar backlog",
                owner="Carlos",
                due_date="2026-03-12",
            ),
            ActionItem(
                description="Confirmar capacidade da equipe",
                owner="João",
                due_date="2026-03-11",
            ),
        ],
    )

    add_meeting(meeting)
    print("Reunião de exemplo adicionada.")


@app.command("list-meetings")
def list_meetings_command():
    print(list_meetings())


if __name__ == "__main__":
    app()