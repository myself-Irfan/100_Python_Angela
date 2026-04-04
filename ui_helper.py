from pathlib import Path
from colour_model import ColourResult


_TEMPLATES_DIR = Path(__file__).parent / "templates"


def _load(filename: str) -> str:
    return (_TEMPLATES_DIR / filename).read_text(encoding="utf-8")


_STRIP_SEGMENT_TMPL: str = _load("strip_segment.html")
_SWATCH_CARD_TMPL: str = _load("swatch_card.html")
_RAW_CSS: str = _load("styles.css")

CSS: str = f"<style>\n{_RAW_CSS}\n</style>"


def colour_strip_html(colours: list[ColourResult]) -> str:
    segments = "".join(
        _STRIP_SEGMENT_TMPL.format(hex=c.hex, percentage=c.percentage)
        for c in colours
    )
    return f'<div class="colour-strip">{segments}</div>'


def swatch_card_html(colour: ColourResult, rank: int, max_pct: float) -> str:
    bar_width = round(min((colour.percentage / max_pct) * 100, 100), 1)
    return _SWATCH_CARD_TMPL.format(
        hex=colour.hex,
        rgb_str=colour.rgb_str,
        percentage=colour.percentage,
        bar_width=bar_width,
        rank=rank,
    )