import pypdf
import pypdf.errors
import textwrap
import structlog

from .text_cleaner_service import TextCleanerService

logger = structlog.get_logger()


class PDFTextExtractorService:
    def __init__(self, chunk_size: int, lookahead_ratio: float, min_break_ratio: float):
        self.chunk_size = chunk_size
        self._lookahead_ratio = lookahead_ratio
        self._min_break_ratio = min_break_ratio
        self._cleaner = TextCleanerService()

    def extract_chunks(self, pdf_file: str):
        with open(pdf_file, "rb") as f:
            reader = pypdf.PdfReader(f)

            if reader.is_encrypted:
                logger.error("Cannot process encrypted PDF", pdf_file=pdf_file)
                raise ValueError("Cannot process encrypted PDF file")

            total_pages = len(reader.pages)
            accumulated_text = ""

            for i, page in enumerate(reader.pages):
                try:
                    page_txt = page.extract_text()
                    if page_txt and page_txt.strip():
                        cleaned = self._cleaner.clean_text(page_txt)
                        if cleaned:
                            accumulated_text += " " + cleaned

                    chunks, accumulated_text = self._split_chunks(accumulated_text)
                    yield from chunks

                    logger.info(
                        'Processing PDF',
                        processed_page=i+1,
                        total_pages=total_pages
                    )
                except pypdf.errors.PdfReadError as err:
                    logger.warning(
                        'Error Processing PDF',
                        page_num=i+1,
                        error=str(err)
                    )

            if accumulated_text.strip():
                yield from textwrap.wrap(accumulated_text, self.chunk_size)

    def _split_chunks(self, text: str) -> tuple[list[str], str]:
        chunks = []

        while len(text) >= self.chunk_size:
            lookahead = int(self.chunk_size * self._lookahead_ratio)
            cut = self._find_break_point(text[:self.chunk_size + lookahead])
            chunks.append(text[:cut].strip())
            text = text[cut:].strip()

        return chunks, text

    def _find_break_point(self, text: str) -> int:
        min_break = int(self.chunk_size * self._min_break_ratio)

        for punct in ['. ', '! ', '? ']:
            pos = text.rfind(punct)
            if pos > min_break:
                return pos + 1
        return self.chunk_size