from pydantic import BaseModel


class ConfigPatchSchema(BaseModel):
    openai_base_url: str | None = None
    openai_api_key: str | None = None
    models: list[str] | None = None
    president_model: str | None = None
    consensus_threshold: float | None = None


class ConfigSchema(BaseModel):
    openai_base_url: str = ""
    openai_api_key: str = ""
    models: list[str] = []
    president_model: str = ""
    consensus_threshold: float = 0.8

    def update(self, patch: ConfigPatchSchema):
        for field, value in patch.model_dump(exclude_unset=True).items():
            setattr(self, field, value)
