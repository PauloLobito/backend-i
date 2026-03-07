
import typer
from src.logic import analyze_text

app = typer.Typer()

@app.command()
def analyze(file: str):
    """Analyze a text file and show statistics."""
    try:
        result = analyze_text(file)
        print(f"Lines: {result['lines']}")
        print(f"Words: {result['words']}")
        print(f"Characters: {result['characters']}")
    except FileNotFoundError:
        print("Error: File not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")