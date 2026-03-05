from typer import Typer
app = Typer(
    name = "FASTAPI CLI",
)

@app.command()
def run():
    ...

if __name__ == "__main__":
        app()