import logging
import requests
from bs4 import BeautifulSoup


def get_req() -> str | None:
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    }

    try:
        resp = requests.get(url=URL, headers=headers)
        resp.raise_for_status()
        logging.info('Request successful')
        return resp.text
    except requests.exceptions.RequestException as req_err:
        logging.warning(f'Request error: {req_err}')
    except Exception as err:
        logging.error(f'Unexpected error: {err}')
    return None


def get_soup(resp: str) -> BeautifulSoup:
    return BeautifulSoup(resp, 'html.parser')

def main():
    soup = get_soup(get_req())

    if soup:
        price = soup.find(class_="a-offscreen").get_text()
        price = price.split('$')[1]
        logging.info(price)
    else:
        logging.warning('No response to scrape')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

    URL = 'https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6'

    main()