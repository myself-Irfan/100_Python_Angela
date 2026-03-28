import json
from dataclasses import dataclass
from pathlib import Path

_CONF_PATH = Path(__file__).parent / "config.json"


@dataclass
class Config:
    chunk_size: int
    lang: str
    max_workers: int
    lookahead_ratio: float
    min_break_ratio: float
    output_name: str
    input_file: str


def load_config() -> Config:
    with open(_CONF_PATH, "r") as f:
        return Config(**json.load(f))