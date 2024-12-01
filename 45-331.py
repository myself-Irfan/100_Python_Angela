import logging
import requests
from bs4 import BeautifulSoup


def get_soup(url: str)-> BeautifulSoup | None:
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, 'html.parser')
    except requests.exceptions.RequestException as req_err:
        logging.error(f'Failed to fetch data from url: {req_err}')
    except Exception as err:
        logging.error(f'Unexpected Error: {err}')
    return None

def get_dict(all_titles: BeautifulSoup) -> dict:
    title_scores = {}

    for title in all_titles:
        title_text = title.find("span", class_="titleline").a.text

        score_row = title.find_next_sibling("tr")
        score_span = score_row.find("span", class_="score")
        score = int(score_span.text.split()[0]) if score_span else 0

        title_scores[title_text] = score

    return title_scores


def main():
    soup_cont = get_soup(URL)

    all_title = soup_cont.find_all(name="tr", class_="athing submission")

    logging.info(get_dict(all_title))


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s -> %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

    URL = 'https://news.ycombinator.com/news'


    main()