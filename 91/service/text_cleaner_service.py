import re


class TextCleanerService:
    _WHITESPACE = re.compile(r"\s+")
    _MISSING_PERIOD = re.compile(r'([a-z])([A-Z])')
    _PUNCT_SPACING = re.compile(r"([.!?])\s*([a-z])")
    _PAGE_NUM_INLINE = re.compile(r"\n\d+\n")
    _PAGE_NUM_TRAILING = re.compile(r"\b\d{1,3}\b(?=\s*$)", re.MULTILINE)

    _REPLACEMENTS = {
        '"':      '"',
        '\u2018': "'",
        '\u2019': "'",
        '–':      '-',
        '—':      '-',
        '…':      '...',
        '\u00a0': ' ',
    }

    def clean_text(self, text: str) -> str:
        text = self._WHITESPACE.sub(" ", text)
        text = self._MISSING_PERIOD.sub(r'\1. \2', text)
        text = self._PUNCT_SPACING.sub(r'\1 \2', text)
        text = self._PAGE_NUM_INLINE.sub(" ", text)
        text = self._PAGE_NUM_TRAILING.sub(" ", text)

        for old, new in self._REPLACEMENTS.items():
            text = text.replace(old, new)

        return text.strip()