from dataclasses import dataclass


@dataclass(frozen=True)
class ColourResult:
    hex: str
    red: int
    green: int
    blue: int
    percentage: float

    @property
    def rgb_str(self) -> str:
        return f"rgb({self.red},{self.green},{self.blue})"

    @property
    def luminance(self) -> float:
        return 0.299 * self.red + 0.587 * self.green + 0.114 * self.blue

    @property
    def is_dark(self) -> bool:
        return self.luminance < 128

    def __str__(self) -> str:
        return f"{self.hex}  {self.rgb_str}  {self.percentage:.1f}%"