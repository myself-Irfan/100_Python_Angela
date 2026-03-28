import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import structlog
from gtts import gTTS
from pydub import AudioSegment

logger = structlog.get_logger()


class AudioConverterService:
    def __init__(self, lang: str, max_workers: int):
        self.lang = lang
        self.max_workers = max_workers

    def convert(self, chunks: list[tuple[int, str]], output_file: str):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_files = self._generate_all(chunks, temp_dir)
            self._combine(temp_files, output_file)

    def _generate_all(self, chunks: list[tuple[int, str]], temp_dir: str) -> list[str]:
        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._generate_one, chunk, idx, temp_dir): idx
                for idx, chunk in chunks
            }
            for future in as_completed(futures):
                idx, path = future.result()
                results.append((idx, path))
                logger.info(
                    'Chunk processed and saved',
                    count=idx+1,
                    path=path
                )

        return [path for _, path in sorted(results)]

    def _generate_one(self, text_chunk: str, idx: int, temp_dir: str) -> tuple[int, str]:
        tts = gTTS(text=text_chunk, lang=self.lang)
        path = Path(temp_dir) / f"part_{idx}.mp3"
        tts.save(str(path))

        return idx, str(path)

    def _combine(self, temp_files: list[str], output_file: str):
        logger.info(
            "Combining audio files",
            file_count=len(temp_files)
        )
        final_audio = AudioSegment.empty()

        for file in temp_files:
            final_audio += AudioSegment.from_mp3(file)
            Path(file).unlink()

        final_audio.export(output_file, format="mp3")
        logger.info(
            "Conversion complete",
            output_file=output_file
        )