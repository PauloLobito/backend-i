from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.api.routers.meetings import router as meetings_router

app = FastAPI(title="Meeting Note Assistant API")


@app.exception_handler(RequestValidationError)
def request_validation_exception_handler(_, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": exc.errors(),
        },
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(meetings_router)