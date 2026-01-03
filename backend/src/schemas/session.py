from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from schemas.message import MessageTreeSchema


class SessionSchema(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str = Field(default="New Session")
    message_tree: MessageTreeSchema
