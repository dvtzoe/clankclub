from typing import Literal, override
from uuid import UUID, uuid4

from openai.types.chat import (
    ChatCompletion,
    ChatCompletionMessageParam,
)
from pydantic import BaseModel, Field


class BaseMessage(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    def to_openai(self) -> ChatCompletionMessageParam:
        raise NotImplementedError


class SystemMessage(BaseMessage):
    role: Literal["system"] = "system"
    content: str

    @override
    def to_openai(self) -> ChatCompletionMessageParam:
        return {"role": self.role, "content": self.content}


class UserMessage(BaseMessage):
    role: Literal["user"] = "user"
    content: str

    @override
    def to_openai(self) -> ChatCompletionMessageParam:
        return {"role": self.role, "content": self.content}


class AssistantMessage(BaseMessage):
    role: Literal["assistant"] = "assistant"

    raw: ChatCompletion

    @property
    def content(self) -> str | None:
        return self.raw.choices[0].message.content if self.raw else None

    @override
    def to_openai(self) -> ChatCompletionMessageParam:
        return {"role": self.role, "content": self.content or ""}


Message = SystemMessage | UserMessage | AssistantMessage

MultiModelMessage = dict[str, Message]


class MessageNode(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    message: Message | MultiModelMessage
    prev: UUID | None = None
    next: list[UUID] = Field(default_factory=list)
    # index of the selected next_node in case of parallel messages
    selected: int = 0


class MessageTreeSchema(BaseModel):
    nodes: dict[UUID, MessageNode] = Field(default_factory=dict)
    root: UUID | None = None

    def add_node(self, node: MessageNode):
        self.nodes[node.id] = node

        return self

    def link(self, prev: UUID, next: UUID):
        self.nodes[prev].next.append(next)
        self.nodes[next].prev = prev

        return self

    def __getitem__(self, key: UUID | int | list[int]) -> UUID:
        if isinstance(key, UUID):
            return self.nodes[key].id
        elif isinstance(key, int):
            node_id = self.root
            if key >= 0:
                for _ in range(key):
                    if (
                        not self.nodes[node_id].next
                        or len(self.nodes[node_id].next) == 0
                    ):
                        raise IndexError("No next nodes available")
                    node_id = self.nodes[node_id].next[self.nodes[node_id].selected]
            else:
                for _ in range(-key):
                    if not node_id:
                        raise Exception("Node ID is None")
                    if not self.nodes[node_id].prev:
                        raise IndexError("No previous nodes available")
                    node_id = self.nodes[node_id].prev
        else:
            node_id = self.root
            for k in key:
                if not self.nodes[node_id].next:
                    raise IndexError("No next nodes available")
                node_id = self.nodes[node_id].next[k]
        if not node_id:
            raise Exception("Node ID is None")
        return node_id

    def end(self, node_id: UUID) -> MessageNode:
        node = self.nodes[node_id]
        while node.next:
            node = self.nodes[node.next[node.selected]]
        return node
