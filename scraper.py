import csv
import re
import time

import requests
import structlog
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from config import HEADERS, NUTRIENT_LABELS, settings
from models import FoodNutrition

log = structlog.get_logger(__name__)


def _to_float(val: str) -> float | None:
    if not val or val.upper() == "N/A":
        return None
    try:
        return float(re.sub(r"[^\d.]", "", val))
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# HTTP client
# ---------------------------------------------------------------------------

class NutritionClient:
    def __init__(self):
        self._session = requests.Session()
        self._session.headers.update(HEADERS)

    @retry(
        retry=retry_if_exception_type(requests.RequestException),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry_error_callback=lambda _: None,
    )
    def get(self, url: str) -> BeautifulSoup | None:
        try:
            resp = self._session.get(url, timeout=settings.req_timeout_sec)
            resp.raise_for_status()
            log.debug("fetch_ok", url=url, status=resp.status_code)
            return BeautifulSoup(resp.text, "html.parser")
        except requests.HTTPError as exc:
            if exc.response is not None and exc.response.status_code == 429:
                retry_after = int(exc.response.headers.get("Retry-After", 60))
                log.warning("rate_limited", url=url, retry_after=retry_after)
                time.sleep(retry_after)
            else:
                log.warning("fetch_failed", url=url, error=str(exc))
            raise  # let tenacity retry
        except requests.RequestException as exc:
            log.warning("fetch_failed", url=url, error=str(exc))
            raise  # let tenacity retry

    def close(self):
        self._session.close()

    def __enter__(self): return self
    def __exit__(self, *_): self.close()


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

class NutritionParser:

    def food_links(self, soup: BeautifulSoup) -> list[tuple[str, str, str]]:
        """
        Returns list of (name, url, protein_value) tuples.

        THE BUG: the table has class="full_width results zero".
        find("table", class_="results") does an exact match on the whole
        class attribute string — it fails when there are multiple classes.

        Fix: use CSS selector  table.results  which correctly matches any
        element whose class list *contains* "results".
        """
        table = soup.select_one("table.results")

        if not table:
            log.error("table_not_found",
                      all_table_classes=[t.get("class") for t in soup.find_all("table")])
            return []

        links = []
        for row in table.select("tr"):
            cells = row.find_all("td")
            if len(cells) < 2:
                continue
            anchor = cells[0].find("a", class_="table_item_name")
            if not anchor:
                continue

            href = anchor["href"]
            url = href if href.startswith("http") else f"{settings.base_url}/{href.lstrip('/')}"
            name = anchor.get_text(strip=True)

            # Grab the protein value already present in the list row —
            # saves one HTTP request per food for the primary nutrient.
            protein = cells[1].get_text(strip=True) if len(cells) > 1 else "N/A"

            links.append((name, url, protein))

        log.info("links_found", count=len(links))
        return links

    def food_detail(self, name: str, url: str, protein_from_list: str, soup: BeautifulSoup) -> FoodNutrition:
        nutrients = {field: _to_float(self._nutrient(soup, label)) for field, label in NUTRIENT_LABELS.items()}

        # Use the list-page protein as a fallback if the detail page parse misses.
        if nutrients.get("protein_g") is None:
            nutrients["protein_g"] = _to_float(protein_from_list)

        return FoodNutrition(
            name=name,
            serving_size_g=self._serving(soup),
            source_url=url,
            **nutrients,
        )

    def _nutrient(self, soup: BeautifulSoup, label: str) -> str:
        label_lower = label.lower()
        for td in soup.find_all("td"):
            cell_text = td.get_text(strip=True).lower()
            if cell_text == label_lower or cell_text.startswith(label_lower + ","):
                if sibling := td.find_next_sibling("td"):
                    return sibling.get_text(strip=True)
        return "N/A"

    def _serving(self, soup: BeautifulSoup) -> str:
        for tag in soup.find_all(["span", "td", "div"]):
            if "serving size" in tag.get_text(strip=True).lower():
                sibling = tag.find_next_sibling()
                if sibling and (val := sibling.get_text(strip=True)):
                    return val
        return "100 g"


# ---------------------------------------------------------------------------
# Scraper orchestrator
# ---------------------------------------------------------------------------

class NutritionScraper:
    def __init__(self, client: NutritionClient, parser: NutritionParser):
        self._client = client
        self._parser = parser

    def run(self, list_url: str, max_foods: int, delay: float, output: str) -> None:
        log.info("scrape_start", max_foods=max_foods, output=output)

        soup = self._client.get(list_url)
        if not soup:
            log.error("list_page_failed")
            return

        links = self._parser.food_links(soup)[:max_foods]
        if not links:
            log.error("no_links_aborting")
            return

        records = self._crawl(links, delay)
        self._save(records, output)
        log.info("scrape_done", saved=len(records))

    def _crawl(self, links: list[tuple[str, str, str]], delay: float) -> list[FoodNutrition]:
        records = []
        total = len(links)
        for i, (name, url, protein) in enumerate(links, 1):
            log.info("scraping", food=name, progress=f"{i}/{total}")
            if soup := self._client.get(url):
                records.append(self._parser.food_detail(name, url, protein, soup))
            else:
                log.warning("skipped", food=name, url=url)
            if i < total:
                time.sleep(delay)
        return records

    def _save(self, records: list[FoodNutrition], path: str) -> None:
        if not records:
            log.warning("nothing_to_save")
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(FoodNutrition.csv_header())
            writer.writerows(r.to_row() for r in records)
        log.info("csv_saved", path=path, rows=len(records))