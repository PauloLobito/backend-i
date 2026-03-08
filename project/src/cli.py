
from unittest import result

import typer
from src.logic import analyze_text  # relativo à pasta src

app = typer.Typer()  


@app.command()
def analyze(
    file: str = typer.Argument(..., help="Path to the text file to analyze")
):
    """Analyze a text file and show statistics."""
    try:
        result = analyze_text(file)
        typer.echo(f"Lines: {result['lines']}")
        typer.echo(f"Words: {result['words']}")
        typer.echo(f"Characters: {result['characters']}")
    except FileNotFoundError:
        typer.echo("Error: File not found.")
    except Exception as e:
        typer.echo(f"Unexpected error: {e}")

        