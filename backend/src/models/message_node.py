import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.mutable import MutableDict, MutableList
from sqlalchemy.orm import Mapped, mapped_column

from models.base import BaseModel


class MessageNodeModel(BaseModel):
    __tablename__: str = "message_node"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    message: Mapped[dict] = mapped_column(
        MutableDict.as_mutable(JSONB),
        nullable=False,
    )

    # Previous node (single parent)
    prev: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("message_nodes.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Next nodes (parallel branches)
    next: Mapped[list[uuid.UUID]] = mapped_column(
        MutableList.as_mutable(JSONB),
        default=list,
    )

    # Selected index among `next`
    selected: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
