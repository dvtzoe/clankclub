from pydantic import BaseModel


class ConfigSchema(BaseModel):
    openai_base_url: str
    openai_api_key: str
    models: list[str]
    president_model: str
    consensus_threshold: float = 0.8


class ConfigPatchSchema(BaseModel):
    openai_base_url: str | None = None
    openai_api_key: str | None = None
    models: list[str] | None = None
    president_model: str | None = None
    consensus_threshold: float | None = None
