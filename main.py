from datetime import datetime
from pathlib import Path
import structlog

from service.pdf_text_extractor_service import PDFTextExtractorService
from service.audio_converter_service import AudioConverterService
from logger import setup_logging
from config import load_config

logger = structlog.get_logger()


def validate_pdf(pdf_file: str):
    pdf_path = Path(pdf_file)

    if not pdf_path.exists():
        logger.warning(
            "PDF file not found",
            pdf_file=pdf_file
        )
        raise FileNotFoundError(f"PDF file not found: {pdf_file}")

    if pdf_path.suffix.lower() != ".pdf":
        logger.warning(
            "File must be PDF format",
            pdf_file=pdf_file
        )
        raise ValueError(f"File must be PDF format: {pdf_file}")


def build_output_filename(name: str | None) -> str:
    stem = name or "audiobook"
    timestamp = datetime.now().strftime("%Y_%m_%d")
    return f"{stem}_{timestamp}.mp3"


def convert_pdf_to_audiobook(pdf_file: str, output_name: str, lang: str, chunk_size: int, max_workers: int, lookahead_ratio: float, min_break_ratio: float):
    logger.info(
        "Converting PDF to Audiobook",
        pdf_file=pdf_file
    )

    validate_pdf(pdf_file)

    output_file = build_output_filename(output_name)
    extractor = PDFTextExtractorService(
        chunk_size=chunk_size,
        lookahead_ratio=lookahead_ratio,
        min_break_ratio=min_break_ratio
    )
    converter = AudioConverterService(
        lang=lang,
        max_workers=max_workers,
    )

    chunks = list(enumerate(extractor.extract_chunks(pdf_file)))

    if not chunks:
        logger.info(
            'No text extracted from file',
            pdf_file=pdf_file
        )
        raise ValueError(f'No text extracted from file: {pdf_file}')

    converter.convert(chunks, output_file)


def main():
    setup_logging()
    config = load_config()

    convert_pdf_to_audiobook(
        pdf_file=config.input_file,
        output_name=config.output_name,
        lang=config.lang,
        chunk_size=config.chunk_size,
        max_workers=config.max_workers,
        lookahead_ratio=config.lookahead_ratio,
        min_break_ratio=config.min_break_ratio,
    )


if __name__ == '__main__':
    main()

# TODO: instead of hardcoded read values from .env or config.json