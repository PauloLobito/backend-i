from datetime import datetime
from typing_extensions import Annotated
import typer

app = typer.Typer(help="CLI para gerir reuniões.")

def validate_date(value: str) -> str:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise typer.BadParameter("Data inválida. Usa o formato YYYY-MM-DD.")
    return value

@app.command("create-meeting")
def create_meeting(
    title: Annotated[
        str,
        typer.Option("--title", help="Título da reunião")
    ],
    date: Annotated[
        str,
        typer.Option("--date", callback=validate_date, help="Data da reunião no formato YYYY-MM-DD")
    ],
    owner: Annotated[
        str,
        typer.Option("--owner", help="Responsável pela reunião")
    ],
) -> None:
    typer.echo("Meeting created successfully!")
    typer.echo(f"Title : {title}")
    typer.echo(f"Date  : {date}")
    typer.echo(f"Owner : {owner}")

if __name__ == "__main__":
    app()


# Para criar uma reunião usando a CLI, execute o seguinte comando no terminal:
#cd session1/meeting-note-assistant/
#python app/cli.py "Sprint Review" 2026-03-10 "Ana"