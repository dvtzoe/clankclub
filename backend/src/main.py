from contextlib import asynccontextmanager

import fastapi

from api.sessions import router as sessions_router
from core.config import Config


@asynccontextmanager
async def lifespan(_app: fastapi.FastAPI):
    Config.load()
    yield


app = fastapi.FastAPI()

app.include_router(sessions_router)
