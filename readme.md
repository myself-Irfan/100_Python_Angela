# PDF to Audiobook Converter

Converts PDF files into MP3 audiobooks using text-to-speech. Text is extracted page by page, cleaned, split into natural-sounding chunks, and converted to audio in parallel before being combined into a single output file.

## Requirements

- Python 3.10+
- [ffmpeg](https://ffmpeg.org/download.html) (required by `pydub` for audio processing)

## Installation

```bash
pip install -r requirements.txt
```

> **Note:** Make sure `ffmpeg` is installed and available on your `PATH`.

## Configuration

Edit `config.json` before running:

```json
{
  "input_file": "input.pdf",
  "output_name": "audiobook",
  "lang": "en",
  "chunk_size": 2000,
  "lookahead_ratio": 0.1,
  "min_break_ratio": 0.7,
  "max_workers": 5
}
```

| Field | Description | Default |
|---|---|---|
| `input_file` | Path to the source PDF | `input.pdf` |
| `output_name` | Stem of the output MP3 filename | `audiobook` |
| `lang` | Language code for TTS (e.g. `en`, `fr`, `de`) | `en` |
| `chunk_size` | Max characters per TTS chunk | `2000` |
| `lookahead_ratio` | Extra characters scanned beyond `chunk_size` to find a natural break | `0.1` |
| `min_break_ratio` | Minimum position (as fraction of `chunk_size`) to accept a sentence break | `0.7` |
| `max_workers` | Parallel threads for TTS generation | `5` |

## Usage

Place your PDF at the path specified in `input_file`, then run:

```bash
python main.py
```

The output file will be saved in the working directory as `{output_name}_{YYYY_MM_DD}.mp3`.

## Project Structure

```
.
├── main.py                          # Entry point
├── config.py                        # Config loader
├── config.json                      # Runtime configuration
├── logger.py                        # Structured logging setup
└── service/
    ├── pdf_text_extractor_service.py  # PDF reading and chunking
    ├── audio_converter_service.py     # TTS and MP3 generation
    └── text_cleaner_service.py        # Text normalisation
```

## How It Works

1. **Extract** — `PDFTextExtractorService` reads the PDF page by page using `pypdf`, skipping encrypted files and pages with read errors.
2. **Clean** — `TextCleanerService` normalises whitespace, fixes missing periods at word boundaries, strips inline page numbers, and replaces typographic characters.
3. **Chunk** — Text is split into chunks no larger than `chunk_size` characters, with breaks preferring sentence endings (`.`, `!`, `?`).
4. **Convert** — `AudioConverterService` sends each chunk to `gTTS` in parallel using a thread pool, saving temporary MP3 files.
5. **Combine** — `pydub` concatenates the temporary files in order into a single output MP3.

## Limitations

- Requires an internet connection (gTTS calls the Google Translate TTS API).
- Encrypted PDFs are not supported.
- Scanned PDFs (image-only) will produce no output, as there is no OCR step.