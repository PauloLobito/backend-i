import typer
from typer import Typer

from core.errors import NotFoundError, ValidationError
from core.validators import validate_iso_date

app = Typer(
    name="FASTAPI CLI",
)

ERROR_CODES = {
    ValidationError: 2,
    NotFoundError: 3,
}


@app.command()
def run():
    import uvicorn
    from api.main import api

    uvicorn.run(api)


@app.command()
def request(date: str):
    try:
        validate_iso_date(date)
        typer.echo("Request válido")
    except (ValidationError, NotFoundError) as exc:
        code = ERROR_CODES.get(type(exc), 1)
        typer.echo(f"Erro: {exc}")
        raise typer.Exit(code=code)


if __name__ == "__main__":
    app()