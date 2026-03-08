import typer

def read_file(filepath: str):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        typer.echo(f"Error: File '{filepath}' not found.")
        raise typer.Exit(1)