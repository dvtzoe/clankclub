from typing import Literal, override

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
    role: Literal["system"] = "system"
    content: str | None

    def to_openai(self) -> ChatCompletionMessageParam:
        return {"role": self.role, "content": self.content or ""}

    @override
    def __str__(self) -> str:
        return f"System: {self.content}"


class UserMessage(BaseModel):
    role: Literal["user"] = "user"
    content: str | None

    def to_openai(self) -> ChatCompletionMessageParam:
        return {"role": self.role, "content": self.content or ""}

    @override
    def __str__(self) -> str:
        return f"User: {self.content}"


class AssistantMessage(BaseModel):
    role: Literal["assistant"] = "assistant"

    reply: ChatCompletion

    @property
    def content(self) -> str | None:
        return self.reply.choices[0].message.content if self.reply else None

    def to_openai(self) -> ChatCompletionMessageParam:
        return {"role": self.role, "content": self.content or ""}

    @override
    def __str__(self) -> str:
        return f"Assistant: {self.content}"


Message = SystemMessage | UserMessage | AssistantMessage

MessagesList = list[list[Message]]
MessagesHistory = list[Message | list[Message]]
