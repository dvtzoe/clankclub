from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.chat import chat
from db import get_db
from schemas.api.chat import ChatRequest

router = APIRouter(prefix="/api/chat")


@router.post("/", status_code=status.HTTP_200_OK)
async def chat_endpoint(
    req: ChatRequest,
    db_session: AsyncSession = Depends(get_db),
):
    """
    Handle chat messages.
    """
    response = await chat(
        user_input=req.user_message,
        session_id=req.session_id,
        db_session=db_session,
    )
    return {"response": response}
