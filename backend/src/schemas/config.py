from pydantic import BaseModel


class Config(BaseModel):
    openai_base_url: str
    openai_api_key: str
    models: list[str]
    president_model: str
    consensus_threshold: float = 0.8
