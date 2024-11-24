import os
import logging
from dotenv import load_dotenv
from google_sheet import GSheetService
import requests


def make_request(exercise_txt: str) -> dict | None:
    headers = {
        'x-app-id': APP_ID,
        'x-app-key': API_KEY
    }

    params = {
        'query': exercise_txt
    }

    try:
        resp = requests.post(url=API_ENDPT, json=params, headers=headers, timeout=API_TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f'HTTP Error: {http_err} | Response: {resp.text}')
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f'Connection Error: {conn_err}')
    except requests.exceptions.Timeout as time_err:
        logging.error(f'Timeout Error: {time_err}')
    except requests.exceptions.RequestException as req_err:
        logging.error(f'Request Error: {req_err}')
    except Exception as err:
        logging.error(f'Unexpected Error: {err}')
        return None


def clean_resp(resp: dict) -> list:
    formatted_data = [['name', 'duration_min', 'met', 'nf_calories']]

    if not resp:
        formatted_data.append(['n/a', 'n/a', 'n/a', 'n/a'])
    else:
        for res in resp.get('exercises', []):
            formatted_data.append([
                res.get('name'),
                res.get('duration_min'),
                res.get('met'),
                res.get('nf_calories')
            ])

    return formatted_data

def main():
    i_sheet = GSheetService()

    # ex_in = input('Input your exercise: ')
    ex_in = 'walked 0.25 km'

    data_to_paste = clean_resp(make_request(ex_in))

    result = i_sheet.paste_data(data=data_to_paste, nw_sheet=False)

    logging.info(f'Result: {result}')


if __name__ == '__main__':
    load_dotenv()

    cur_f_name = os.path.splitext(os.path.basename(__file__))[0]

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(funcName)s | %(message)s',
        handlers={
            logging.StreamHandler(),
            logging.FileHandler(f'{cur_f_name}.log')
        }
    )

    APP_ID = os.getenv('NUTRITION_APP_ID')
    API_KEY = os.getenv('NUTRITION_API_KEY')
    API_ENDPT = os.getenv('NUTRITION_API_ENDPT')
    API_TIMEOUT = int(os.getenv('TIMEOUT_MS'))

    main()
