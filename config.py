from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_title: str
    app_icon: str
    app_layout: str
    app_caption: str

    default_n_colours: int
    min_colours: int
    max_colours: int
    sample_size: int
    kmeans_random_state: int

    allowed_extensions: list[str]


def _load_settings() -> Settings:
    return Settings(
        app_title="iPaletteFinder",
        app_icon="🎨",
        app_layout="centered",
        app_caption="Find palettes from image",
        default_n_colours=int(os.environ.get("DEFAULT_N_COLOURS")),
        min_colours=int(os.environ.get("MIN_COLOURS")),
        max_colours=int(os.environ.get("MAX_COLOURS")),
        sample_size=int(os.environ.get("SAMPLE_SIZE")),
        kmeans_random_state=int(os.environ.get("KMEANS_RANDOM_STATE")),
        allowed_extensions=os.environ.get("ALLOWED_EXTENSIONS").split(","),
    )

settings = _load_settings()