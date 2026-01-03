from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from models.session import SessionModel
from schemas.message import MessageTreeSchema, SystemMessage
from schemas.session import SessionSchema

router = APIRouter(prefix="/api/sessions")


@router.get("/new", status_code=status.HTTP_200_OK)
async def new_session(db_session: AsyncSession = Depends(get_db)):
    """
    Create a new session.
    """
    session_schema = SessionSchema(
        message_tree=MessageTreeSchema(root=SystemMessage(content="").id)
    )

    session = SessionModel(**session_schema.model_dump(mode="json"))
    await session.save(db_session)
    return session
