from typer import Typer, echo, style, colors
from datetime import datetime
from dataclasses import dataclass
from pydantic import BaseModel, Field


@dataclass
class Meeting():
    title: str
    owner: str
    date: str = datetime.now().strftime("%d/%m/%Y %H:%M")


cli = Typer()


@cli.command()
def greetings(name: str, surname: str) -> None:
    echo(style(f"Greetings {name} {surname}", fg=colors.BLUE))


@cli.command()
def goodbye(name: str, surname: str) -> None:
    echo(style(f"GoodBye {name} {surname}", fg=colors.RED))


@cli.command()
def create_meeting(title: str, owner: str):

    meeting = Meeting(title=title, owner=owner)

    echo(style(f"""
    ===========================================
               {meeting.title}
    ===========================================
    created by {meeting.owner} on {meeting.date}
        """, fg=colors.BRIGHT_CYAN, bold=True))


if __name__ == "__main__":
    cli()
