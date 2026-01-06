from contextlib import asynccontextmanager

import fastapi

from api.chat import router as chat_router
from api.config import router as config_router
from api.sessions import router as sessions_router
from core.config import Config


@asynccontextmanager
async def lifespan(_app: fastapi.FastAPI):
    Config.load()
    yield


app = fastapi.FastAPI(lifespan=lifespan)

app.include_router(chat_router)
app.include_router(config_router)
app.include_router(sessions_router)
