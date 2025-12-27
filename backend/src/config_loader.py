import json
import os

from dotenv import load_dotenv

from schemas import Config

load_dotenv()
with open(os.getenv("CONFIG_PATH") or r"../config.json", "r") as config_file:
    config = Config(**json.load(config_file))  # pyright: ignore[reportAny]
