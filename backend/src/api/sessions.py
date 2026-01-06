from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from models.session import SessionModel

router = APIRouter(prefix="/api/sessions")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_sessions(db_session: AsyncSession = Depends(get_db)):
    """
    Retrieve all sessions.
    """
    stmt = select(
        SessionModel.id,
        SessionModel.title,
        SessionModel.updated_at,
    )
    result = await db_session.execute(stmt)
    sessions = []
    for row in result.all():
        sessions.append(
            {
                "id": row.id,  # pyright: ignore[reportAny]
                "title": row.title,  # pyright: ignore[reportAny]
                "updated_at": row.updated_at,  # pyright: ignore[reportAny]
            }
        )

    return sessions


@router.get("/{session_id}", status_code=status.HTTP_200_OK)
async def get_session(session_id: str, db_session: AsyncSession = Depends(get_db)):
    """
    Retrieve a session by ID.
    """
    session = await db_session.get(SessionModel, session_id)
    if not session:
        return {"error": "Session not found"}, status.HTTP_404_NOT_FOUND

    return session
