import typer

app = typer.Typer()

@app.command("create-meeting")
def create_meeting(title: str, date: str, owner: str):
    typer.echo("Meeting created successfully!")
    typer.echo(f"Title: {title}")
    typer.echo(f"Date: {date}")
    typer.echo(f"Owner: {owner}")

if __name__ == "__main__":
    app()