import logging
import re
import sys
import tempfile
from pathlib import Path
from typing import List

from gtts import gTTS
from pydub import AudioSegment
import os
import textwrap
import PyPDF2
import structlog


class PDFAudiobookConverter:
    def __init__(self):
        self.chunk_size: int = 2000
        self.lang: str = "en"
        self.max_workers = 5
        self.temp_dir = tempfile.mkdtemp()
        self.logger = self.__setup_logging()

    def __setup_logging(self) -> structlog.BoundLogger:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.set_exc_info,
                structlog.processors.TimeStamper(fmt="ISO", utc=False),
                structlog.dev.ConsoleRenderer(colors=True)
            ],
            wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
            logger_factory=structlog.WriteLoggerFactory(file=sys.stderr),
            cache_logger_on_first_use=False
        )

        return structlog.get_logger(__name__)

    def validate_pdf(self, pdf_file: str) -> bool:
        pdf_path = Path(pdf_file)

        if not pdf_path.exists():
            self.logger.warning(f"PDF file not found: {pdf_file}")
            return False

        if not pdf_path.suffix.lower() == ".pdf":
            self.logger.warning(f"File must be PDF format: {pdf_file}")
            return False

        return True

    def extract_text_chunks(self, pdf_file: str):
        with open(pdf_file, "rb") as f:
            reader = PyPDF2.PdfReader(f)

            if reader.is_encrypted:
                self.logger.error("Cannot process encrypted PDF", pdf_file=pdf_file)
                raise ValueError("Cannot process encrypted PDF file")

            total_pages = len(reader.pages)
            accumulated_text = ""

            for i, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        cleaned_txt = self.__clean_text(page_text)
                        if cleaned_txt:
                            accumulated_text += " " + cleaned_txt

                    while len(accumulated_text) >= self.chunk_size:
                        break_point = self._find_break_point(accumulated_text[:self.chunk_size + 200])

                        if break_point > 0:
                            yield accumulated_text[:break_point].strip()
                            accumulated_text = accumulated_text[break_point:].strip()
                        else:
                            yield accumulated_text[:self.chunk_size].strip()
                            accumulated_text = accumulated_text[self.chunk_size:].strip()

                    self.logger.info("PDF processing progress", processed_page=i + 1, total_pages=total_pages)
                except Exception as err:
                    self.logger.warning("Error processing page", page_num=i + 1, error=str(err))
                    continue

            # Yield any remaining text
            if accumulated_text.strip():
                # Split remaining text into chunks if needed
                remaining_chunks = textwrap.wrap(accumulated_text, self.chunk_size)
                for chunk in remaining_chunks:
                    yield chunk

    def _find_break_point(self, text: str) -> int:
        """
        Find a good break point at the end of a sentence.
        """
        # Look for sentence endings in reverse
        for punct in ['. ', '! ', '? ']:
            pos = text.rfind(punct)
            if pos > self.chunk_size * 0.5:  # At least 50% through chunk
                return pos + 1
        return -1

    def __generate_audio_chunk(self, text_chunk: str, idx: int) -> str:
        tts = gTTS(text=text_chunk, lang=self.lang)
        temp_file = os.path.join(self.temp_dir, f"part_{idx}.mp3")
        tts.save(temp_file)

        return temp_file

    def __combine_audio_chunks(self, temp_files: List[str], audio_file: str):
        self.logger.info("Combining audio files...")

        final_audio = AudioSegment.empty()

        for file in temp_files:
            final_audio += AudioSegment.from_mp3(file)
            os.remove(file)

        final_audio.export(audio_file, format="mp3")

        self.logger.info("File combination success", output_file=audio_file)

    def __clean_text(self, text: str) -> str:
        """
        Clean and normalize text for better TTS output
        """
        # Cleanup excessive whitespace
        text = re.sub(r"\s+", " ", text)
        # Add periods between sentences
        text = re.sub(r'([a-z])([A-Z])', r'\1. \2', text)
        # Fix spacing after punctuation
        text = re.sub(r"([.!?])\s*([a-z])", r"\1 \2", text)
        # Remove page numbers on separate lines
        text = re.sub(r"\n\d+\n", " ", text)
        # End of line page numbers
        text = re.sub(r"\b\d{1,3}\b(?=\s*$)", " ", text, flags=re.MULTILINE)

        replacements = {
            '"': '"',
            ''': "'", 
            ''': "'",  # Smart quotes
            '–': '-',
            '—': '-',  # Em/en dashes
            '…': '...',  # Ellipsis
            '\u00a0': ' ',  # Non-breaking space
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text.strip()

    def convert_pdf_to_audio(self, pdf_file: str, audio_file: str = "audiobook.mp3"):
        self.logger.info("Initiating conversion")

        if not self.validate_pdf(pdf_file):
            self.logger.warning(f"Please try again")

        temp_files = []

        for i, chunk in enumerate(self.extract_text_chunks(pdf_file)):
            temp_file = self.__generate_audio_chunk(chunk, i)
            temp_files.append(temp_file)
            chunk_count = i + 1
            self.logger.info("Chunk processed and saved", count=f"{chunk_count}")

        if not temp_files:
            self.logger.error(f"No audio chunk generated", pdf_file=pdf_file)
            raise ValueError(f"No audio generated from PDF file {pdf_file}")

        self.__combine_audio_chunks(temp_files, audio_file)


def main():
    pdf_audio_converter = PDFAudiobookConverter()

    pdf_to_read = "input.pdf"
    pdf_audio_converter.convert_pdf_to_audio(pdf_to_read)


if __name__ == "__main__":
    main()