import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from app.api.exceptions import ApiException
from app.api.v1.schemas import BaseErrorResponse
from app.config import Config
from app.api.v1.routers import (
    tweets_router,
    users_router,
    medias_router,
)

app = FastAPI()


# Ловитель ошибок, которые учтены в ApiException
@app.exception_handler(ApiException)
async def api_exception_handler(request: Request, exc: ApiException):
    return JSONResponse(status_code=400, content=exc.to_dict())


# Ловитель всех остальных ошибок
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    error_type = "APIError"
    error_message = str(exc)
    return JSONResponse(
        status_code=500,
        content=BaseErrorResponse(
            error_type=error_type,
            error_message=error_message
        ).model_dump()
    )

# Регистрация роутеров
app.include_router(tweets_router.router, prefix="/api/tweets", tags=["Tweets"])
app.include_router(users_router.router, prefix="/api/users", tags=["Users"])
app.include_router(medias_router.router, prefix="/api/medias", tags=["Medias"])

# Подцепляем frontend
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
app.mount(
    "/", StaticFiles(directory=frontend_path, html=True), name="frontend"
)


if __name__ == "__main__":
    import uvicorn

    Config.log_config()
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
