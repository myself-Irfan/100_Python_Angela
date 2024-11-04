import logging
from os import getenv, path
import requests
from dotenv import load_dotenv


def get_stock_info() -> dict | None:
    logging.info('Initiating call to retrieve stock info')

    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': STOCK_NAME,
        'apikey': STOCK_KEY
    }

    try:
        resp = requests.get(url=STOCK_URL, params=params, timeout=5)
        resp.raise_for_status()
        time_data = resp.json().get(INIT_KEY)

        if not time_data:
            raise KeyError(f'{INIT_KEY} not found | Request: {resp.headers} |Response: {resp.json()}')

        return time_data
    except KeyError as key_err:
        logging.warning(key_err)
    except requests.exceptions.HTTPError as http_err:
        logging.error(f'HTTP Error: {http_err}')
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f'Connection Error: {conn_err}')
    except requests.exceptions.Timeout as time_err:
        logging.error(f'Timeout Error: {time_err}')
    except requests.exceptions.JSONDecodeError as json_err:
        logging.error(f'JSON Decoder Error: {json_err}')
    except requests.exceptions.RequestException as req_err:
        logging.error(f'Request Error: {req_err}')
    except Exception as e:
        logging.error(f'Unexpected Error: {e}')

    return None


def get_latest_n(api_resp: dict, n: int = 1) -> list[float] | None:
    logging.info('Initiating stock response cleanup')

    if not api_resp:
        logging.warning('API Response is null')
        return None

    if n < 1:
        raise ValueError(f'RESP_LEN can not be less than 1: Received {n}')
    elif n > len(api_resp):
        raise ValueError(f'RESP_LEN can not be greater than resp_len | API Len: {len(api_resp)} | Received: {n}')

    dt_li = list(api_resp.keys())[:n]
    try:
        return [round(float(api_resp.get(dt).get(FIN_KEY)), 2) for dt in dt_li]
    except ValueError as val_err:
        logging.error(f'Value Error: {val_err}')
    except TypeError as type_err:
        logging.error(f'Type Error: {type_err}')
    except Exception as err:
        logging.error(f'Unexpected Error: {err}')

    return None


def get_abs_dff(price_li: list[float]) -> float | None:
    logging.info(f'Calculating avg of diff of {price_li}')

    logging.debug(f'Price List: {price_li}')

    if not price_li or len(price_li) < 2:
        return None if not price_li else price_li[0]

    abs_dff = [abs(price_li[i] - price_li[i + 1]) / price_li[i] * 100 for i in range(len(price_li) - 1)]
    return round(sum(abs_dff) / len(abs_dff), 2)


def get_news():
    logging.info('Initiating')

    params = {
        'apiKey': NEWS_KEY,
        'qInTitle': COMP_NAME
    }

    try:
        resp = requests.get(url=NEWS_API, params=params, timeout=5)
        resp.raise_for_status()
        news_resp = resp.json().get('articles')

        if not news_resp:
            raise KeyError('Key "Article" not found')

        return news_resp
    except KeyError as key_err:
        logging.error(f'Key Error: {key_err}')
    except requests.exceptions.HTTPError as http_err:
        logging.error(f'HTTP Error: {http_err}')
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f'Connection Error: {conn_err}')
    except requests.exceptions.Timeout as time_err:
        logging.error(f'Timeout Error: {time_err}')
    except requests.exceptions.JSONDecodeError as json_err:
        logging.error(f'JSON Decoder Error: {json_err}')
    except requests.exceptions.RequestException as req_err:
        logging.error(f'Request Error: {req_err}')
    except Exception as e:
        logging.error(f'Unexpected Error: {e}')

    return None


def clean_news(news_resp: list[dict], n: int = 3):
    logging.info('Cleaning up data for news response')

    return [{'title': article.get('title', 'N/A'), 'description': article.get('description', 'N/A')} for article in news_resp[:n]]


def main():
    api_resp = get_stock_info()
    if api_resp:
        price_li = get_latest_n(api_resp, 2)
        if get_abs_dff(price_li) > 0:
            print(clean_news(get_news()))
        else:
            logging.info('Not worth checking news')
    else:
        logging.error('API response is None')


if __name__ == '__main__':
    cur_f_name = path.splitext(path.basename(__file__))[0]

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s | %(funcName)s -> %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f'{cur_f_name}.log')
        ]
    )

    load_dotenv()

    STOCK_URL = getenv('STOCK_API_URL')
    STOCK_KEY = getenv('STOCK_API_KEY')
    STOCK_NAME = 'TSLA'
    RESP_LEN = 1

    INIT_KEY = 'Time Series (Daily)'
    FIN_KEY = '4. close'

    NEWS_API = getenv('NEWS_API_URL')
    NEWS_KEY = getenv('NEWS_API_KEY')
    COMP_NAME = 'Tesla Inc'

    main()
