import logging
import structlog
import structlog.dev

from config import settings
from scraper import NutritionClient, NutritionParser, NutritionScraper


def configure_logging():
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    )


def main():
    configure_logging()

    with NutritionClient() as client:
        NutritionScraper(client, NutritionParser()).run(
            list_url=settings.list_url,
            max_foods=settings.max_foods,
            delay=settings.crawl_delay_sec,
            output=settings.output_csv,
        )


if __name__ == "__main__":
    main()