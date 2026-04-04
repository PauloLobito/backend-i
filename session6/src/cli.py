import logging

import typer
from typer import Typer

from core.logging_config import configure_logging
from core.errors import NotFoundError, ValidationError
from core.validators import validate_iso_date

configure_logging()
logger = logging.getLogger(__name__)

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

    logger.info("Starting API server")
    uvicorn.run(api)


@app.command()
def request(date: str):
    logger.info("Processing request with date=%s", date)

    try:
        validate_iso_date(date)
        logger.info("Date validated successfully: %s", date)
        typer.echo("Request válido")
    except ValidationError as exc:
        logger.warning("Invalid input received: %s", exc)
        code = ERROR_CODES.get(type(exc), 1)
        typer.echo(f"Erro: {exc}")
        raise typer.Exit(code=code)
    except NotFoundError as exc:
        logger.error("Resource not found: %s", exc)
        code = ERROR_CODES.get(type(exc), 1)
        typer.echo(f"Erro: {exc}")
        raise typer.Exit(code=code)


if __name__ == "__main__":
    app()