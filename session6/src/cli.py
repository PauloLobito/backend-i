from typer import Typer
from api.main import api
from uvicorn import uvicorn


app = Typer(
    name = "MyMeetings API CLI",
)

@app.command()
def run():
    uvicorn.run(api)


if __name__ == "__main__":
    app()