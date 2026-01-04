from fastapi import APIRouter, status

from core.config import Config

router = APIRouter(prefix="/api/config")


@router.get("/", status_code=status.HTTP_200_OK)
def get_config():
    return Config.get()
