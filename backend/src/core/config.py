import json
import os
from pathlib import Path
from threading import Lock

from dotenv import load_dotenv

from schemas.config import ConfigPatchSchema, ConfigSchema

load_dotenv()

CONFIG_PATH = Path(os.getenv("CONFIG_PATH") or r"config.json")


class Config:
    _config: ConfigSchema = ConfigSchema()
    _lock: Lock = Lock()

    @classmethod
    def load(cls) -> ConfigSchema:
        with cls._lock:
            cls._config = ConfigSchema(**json.loads(CONFIG_PATH.read_text()))  # pyright: ignore[reportAny]
            return cls._config

    @classmethod
    def get(cls) -> ConfigSchema:
        if not cls._config:
            cls.load()
        return cls._config

    @classmethod
    def update(cls, patch: ConfigPatchSchema) -> ConfigSchema:
        with cls._lock:
            cls._config.update(patch)
            CONFIG_PATH.write_text(json.dumps(cls._config, indent=2))
            return cls._config
