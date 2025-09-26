import logging
import re
import sys
from pathlib import Path
from gtts import gTTS
from pydub import AudioSegment
import os
import textwrap
import PyPDF2
import structlog


class PDFAudiobookConverter:
    def __init__(self):
        self.chunk_size: int = 1000
        self.lang: str = "en"
        self.logger = self.__setup_logging()

    def __setup_logging(self):
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

    def extract_audiobook(self, pdf_file: str) -> str:
        with open(pdf_file, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "

        if not text.strip():
            raise ValueError(f"No text could be extracted from the PDF file {pdf_file}")

        return self.clean_text(text)

    def validate_pdf(self, pdf_file: str) -> bool:
        pdf_path = Path(pdf_file)
        if not pdf_path.exists():
            self.logger.warning(f"PDF file not found: {pdf_file}")
            return False

        if not pdf_path.suffix.lower() == ".pdf":
            self.logger.warning(f"File must be PDF format: {pdf_file}")
            return False

        return True

    def clean_text(self, text: str) -> str:
        """
        clean and normalize text for better TTS output
        """

        # cleanup excessive whitespace
        text = re.sub(r"\s+", " ", text)
        # add periods between sentences
        text = re.sub(r'([a-z])([A-Z])', r'\1. \2', text)
        # fix spacing after punctuation
        text = re.sub(r"([.!?])\s*([a-z])", r"\1 \2", text)
        # remove page numbers on separate lines
        text = re.sub(r"\n\d+\n", " ", text)
        # end of line page numbers
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

    def conv_txt_audio(self, text: str, audio_file: str = "audiobook.mp3"):
        self.logger.info("Initiating conversion")

        chunks = textwrap.wrap(text, self.chunk_size)
        temp_files = []

        for i, chunk in enumerate(chunks):
            tts = gTTS(text=chunk, lang=self.lang)
            temp_file = f"part_{i}.mp3"
            tts.save(temp_file)
            temp_files.append(temp_file)
            self.logger.info(f"Chunk {i+1}/{len(chunks)} saved as {temp_file}")

        final_audio = AudioSegment.empty()
        for file in temp_files:
            final_audio += AudioSegment.from_mp3(file)

        final_audio.export(audio_file, format="mp3")
        self.logger.info(f"Audiobook saved as {audio_file}")

        for file in temp_files:
            os.remove(file)

def main():
    pdf_audio_converter = PDFAudiobookConverter()

    pdf_to_read = "input.pdf"
    if pdf_audio_converter.validate_pdf(pdf_to_read):
        input_txt = pdf_audio_converter.extract_audiobook(pdf_to_read)
        pdf_audio_converter.conv_txt_audio(input_txt)
    else:
        pdf_audio_converter.logger.info("Please try again")

if __name__ == "__main__":
    main()