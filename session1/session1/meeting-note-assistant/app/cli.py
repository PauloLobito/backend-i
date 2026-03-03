from datetime import datetime
from typing import Annotated
import typer

app = typer.Typer()


@app.command()
def create_meeting(title: str, date: str, owner: str) -> None:
    print(title , date , owner)
    typer.echo(f"Hello from Typer!!!")
    
@app.command()
def main(
        launch_date : Annotated[
            datetime,
            typer.Argument(
                formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%m/%d/%Y"]
            )
        ]
):
    print("Tenta novamente!")


if __name__ == "__main__":
    app()
