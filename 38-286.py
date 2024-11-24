import os
import logging
from dotenv import load_dotenv
from google_sheet import GSheetService
import requests


class NutritionixService:
    def __init__(self):
        self.app_id = os.getenv('NUTRITION_APP_ID')
        self.api_key = os.getenv('NUTRITION_API_KEY')
        self.api_endpt = os.getenv('NUTRITION_API_ENDPT')
        self.api_timeout = int(os.getenv('TIMEOUT_MS'))

    def _make_req(self, exercise_txt: str) -> dict | None:
        headers = {
            'x-app-id': self.app_id,
            'x-app-key': self.api_key
        }

        params = {
            'query': exercise_txt
        }

        try:
            resp = requests.post(url=self.api_endpt, json=params, headers=headers, timeout=self.api_timeout)
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

    def _clean_api_resp(self, resp: dict | None) -> list:
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

    def get_exercise_data(self, ex_in) -> list:
        return self._clean_api_resp(self._make_req(ex_in))


def main():
    i_ex = NutritionixService()
    i_sheet = GSheetService()

    # ex_in = input('Input your exercise: ')
    ex_in = 'walked 0.25 km'

    data_to_paste = i_ex.get_exercise_data(ex_in)

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

    main()
