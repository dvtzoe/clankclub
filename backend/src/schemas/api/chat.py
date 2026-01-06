from uuid import UUID

from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_message: str
    session_id: UUID | None = None


class ChatResponse(BaseModel):
    response: str
