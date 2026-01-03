from pydantic import BaseModel, Field


class DiscussRequest(BaseModel):
    query: str = Field(..., description="The user's query for discussion")
