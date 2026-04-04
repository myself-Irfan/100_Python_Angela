import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

from config import settings
from colour_model import ColourResult


class ColourService:
    def __init__(self):
        self._sample_size =  settings.sample_size
        self._random_state = settings.kmeans_random_state

    def _preprocess(self, image: Image.Image) -> np.ndarray:
        img = image.convert('RGB')
        img.thumbnail((self._sample_size, self._sample_size), Image.LANCZOS)
        return np.array(img).reshape(-1, 3).astype(np.float32)

    def _cluster(self, pixels: np.ndarray, n_cluster: int) -> tuple[np.ndarray, np.ndarray]:
        kmeans = KMeans(
            n_clusters=n_cluster,
            random_state=self._random_state,
            n_init="auto"
        )
        kmeans.fit(pixels)
        return kmeans.cluster_centers_.astype(int), kmeans.labels_

    def _build_results(
            self,
            centers: np.ndarray,
            labels: np.ndarray,
            n_colors: int
    ) -> list[ColourResult]:
        total = len(labels)
        counts = np.bincount(labels, minlength=n_colors)
        order = np.argsort(-counts) # descending by frequency

        results = []
        for idx in order:
            red, green, blue = (int(v) for v in centers[idx])
            percentage = round(float(counts[idx])/total * 100, 1)
            results.append(
                ColourResult(
                    hex=f"#{red:02X}{green:02X}{blue:02X}",
                    red=red,
                    green=green,
                    blue=blue,
                    percentage=percentage,
                )
            )
        return results

    def extract(self, image: Image.Image, n_colors: int) -> list[ColourResult]:
        pixels = self._preprocess(image)
        centres, labels = self._cluster(pixels, n_colors)
        return self._build_results(centres, labels, n_colors)

    @staticmethod
    def to_palette_txt(colors: list[ColourResult]) -> str:
        return "\n".join(str(c) for c in colors)