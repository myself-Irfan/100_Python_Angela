from dataclasses import dataclass, fields, astuple
from typing import Optional


@dataclass
class FoodNutrition:
    name: str
    serving_size_g: str
    calories: Optional[float]
    protein_g: Optional[float]
    fat_g: Optional[float]
    carbohydrate_g: Optional[float]
    fiber_g: Optional[float]
    sugars_g: Optional[float]
    sodium_mg: Optional[float]
    calcium_mg: Optional[float]
    iron_mg: Optional[float]
    potassium_mg: Optional[float]
    vitamin_c_mg: Optional[float]
    source_url: str

    @classmethod
    def csv_header(cls) -> list[str]:
        return [f.name for f in fields(cls)]

    def to_row(self) -> tuple:
        return astuple(self)