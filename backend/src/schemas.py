from typing import Literal
from uuid import UUID, uuid4

from openai.types.chat import (
    ChatCompletion,
    ChatCompletionMessageParam,
)
from pydantic import BaseModel


class Config(BaseModel):
    openai_base_url: str
    openai_api_key: str
    models: list[str]
    president_model: str
    consensus_threshold: float = 0.8


class DiscussRequest(BaseModel):
    query: str


class SystemMessage(BaseModel):
    id: UUID = uuid4()
    role: Literal["system"] = "system"
    content: str

    def to_openai(self) -> ChatCompletionMessageParam:
        return {"role": self.role, "content": self.content}


class UserMessage(BaseModel):
    id: UUID = uuid4()
    role: Literal["user"] = "user"
    content: str

    def to_openai(self) -> ChatCompletionMessageParam:
        return {"role": self.role, "content": self.content}


class AssistantMessage(BaseModel):
    id: UUID = uuid4()
    role: Literal["assistant"] = "assistant"

    raw: ChatCompletion

    @property
    def content(self) -> str | None:
        return self.raw.choices[0].message.content if self.raw else None

    def to_openai(self) -> ChatCompletionMessageParam:
        return {"role": self.role, "content": self.content or ""}


Message = SystemMessage | UserMessage | AssistantMessage


class MessagesHistoryNode(BaseModel):
    id: UUID = uuid4()
    message_id: UUID | list[UUID]
    next_node: list[UUID] | None = None


MessagesHistory = list[MessagesHistoryNode]


class Session(BaseModel):
    id: UUID = uuid4()
    title: str = "New Session"
    messages_history: MessagesHistory
