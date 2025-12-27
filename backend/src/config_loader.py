import json

from schemas import Config

with open(r"../config.json", "r") as config_file:
    config = Config(**json.load(config_file)["backend"])  # pyright: ignore[reportAny]
