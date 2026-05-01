from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="WEBSCRAPE_",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    base_url: str
    crawl_delay_sec: float
    max_foods: int
    req_timeout_sec: int
    output_filename: str
    list_url_path: str = "foods_by_Protein_content.html"

    @computed_field
    @property
    def list_url(self) -> str:
        return f"{self.base_url}/{self.list_url_path}"

    @computed_field
    @property
    def output_csv(self) -> str:
        return f"{self.output_filename}.csv"


settings = Settings()

# Static — not worth putting in .env
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

NUTRIENT_LABELS = {
    "calories":       "Calories",
    "protein_g":      "Protein",
    "fat_g":          "Total Fat",
    "carbohydrate_g": "Carbohydrate",
    "fiber_g":        "Dietary fiber",
    "sugars_g":       "Sugars",
    "sodium_mg":      "Sodium",
    "calcium_mg":     "Calcium",
    "iron_mg":        "Iron",
    "potassium_mg":   "Potassium",
    "vitamin_c_mg":   "Vitamin C",
}