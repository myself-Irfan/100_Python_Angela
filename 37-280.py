import logging
import os.path
from datetime import datetime
from os import getenv
import requests
from dotenv import load_dotenv


class PixelaService:
    def __init__(self):
        logging.debug(f'Initiating')

        self._username: str = PIXELA_USR
        self._password: str = PIXELA_PWD

        self._base_url: str = BASE_URL
        self.graph_col: str = GRPH_COLOR
        self._timeout: int = 10

    def __build_url(self, base_url, endpt: str = None) -> str:
        logging.debug('Building request')

        return f'{base_url}/{endpt}' if endpt else base_url

    def __send_req(self, method: str, url: str, payload=None, headers=None) -> dict:
        response = {}

        if method not in ['POST', 'GET', 'PUT', 'DELETE']:
            logging.error(f'Unsupported HTTP method: {method}')
            return response

        try:
            if method == 'POST':
                response = requests.post(url, json=payload, headers=headers, timeout=self._timeout)
            elif method == 'PUT':
                response = requests.put(url, json=payload, headers=headers, timeout=self._timeout)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=self._timeout)
            else:
                response = requests.get(url, headers=headers, timeout=self._timeout)

            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as http_err:
            logging.error(f'HTTP Error: {http_err} | Response: {response.text}')
        except requests.exceptions.ConnectionError as conn_err:
            logging.error(f'Connection Error: {conn_err}')
        except requests.exceptions.Timeout as time_err:
            logging.error(f'Timeout Error: {time_err}')
        except requests.exceptions.RequestException as req_err:
            logging.error(f'Request Error: {req_err}')
        except Exception as err:
            logging.error(f'Unexpected Error: {err}')

        return response.json()

    def reg_usr(self) -> bool:
        url = self.__build_url(self._base_url)

        payload = {
            "username": self._username,
            "token": self._password,
            "agreeTermsOfService": "yes",
            "notMinor": "yes"
        }

        logging.debug(f'Constructed request: {url} | {payload}')

        response = self.__send_req('POST', url, payload)

        if response.get('isSuccess'):
            logging.info('User registration successfully executed')
            return True
        else:
            logging.warning(f'Registration error: {response}')
            return False

    def create_graph(self) -> bool:
        url = self.__build_url(self._base_url, f'{self._username}/graphs')

        headers = {
            'X-USER-TOKEN': self._password
        }

        body = {
            'id': GRPH_ID,
            'name': 'c0d3grAph',
            'unit': 'minute',
            'type': 'int',
            'color': GRPH_COLOR
        }

        logging.debug(f'Constructed request: {url} | {headers} | {body}')

        response = self.__send_req('POST', url, body, headers)

        if response.get('isSuccess'):
            logging.info('Graph creation successfully executed')
            return True
        else:
            logging.warning(f'Graph creation error: {response}')
            return False

    def post_pixl(self, dt_act: int, quantity: str) -> bool:
        url = self.__build_url(self._base_url, f'{self._username}/graphs/{GRPH_ID}')

        headers = {
            'X-USER-TOKEN': self._password
        }

        body = {
            'date': dt_act,
            'quantity': str(quantity)
        }

        logging.info(f'Constructed request: {url} | {headers} | {body}')

        response = self.__send_req('POST', url, body, headers)

        if response.get('isSuccess'):
            logging.info('Graph update successfully executed')
            return True
        else:
            logging.warning(f'Graph update error: {response}')
            return False

    def put_pixl(self, dt_act: int, quantity: str) -> bool:
        url = self.__build_url(self._base_url, f'{self._username}/graphs/{GRPH_ID}/{dt_act}')

        headers = {
            'X-USER-TOKEN': self._password
        }

        body = {
            'quantity': str(quantity)
        }

        logging.info(f'Constructed request: {url} | {headers} | {body}')

        response = self.__send_req('PUT', url, body, headers)

        if response.get('isSuccess'):
            logging.info(f'Pixel for {dt_act} updated')
            return True
        else:
            logging.warning(f'Pixel update error: {response}')
            return False

    def del_pixl(self, dt_act: str) -> bool:
        url = self.__build_url(self._base_url, f'{self._username}/graphs/{GRPH_ID}/{dt_act}')

        headers = {
            'X-USER-TOKEN': self._password
        }

        response = self.__send_req('DELETE', url, headers=headers)

        if response.get('isSuccess'):
            logging.info(f'Pixel removal for {dt_act} successful')
            return True
        else:
            logging.warning(f'Pixel removal error: {response}')
            return False


def main():
    logging.info(f'Initiating {cur_f_name}')

    date_of_task = datetime.now().strftime('%Y%m%d')

    iPixela = PixelaService()
    # iPixela.reg_usr()
    # iPixela.create_graph()
    # iPixela.post_pixl(date_of_task, 20)
    # iPixela.put_pixl(date_of_task, 40)
    # iPixela.del_pixl(date_of_task)


if __name__ == '__main__':
    cur_f_name = os.path.splitext(os.path.basename(__file__))[0]

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s | %(funcName)s -> %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f'{cur_f_name}.log')
        ]
    )

    load_dotenv()

    PIXELA_USR = 'irfan101'
    PIXELA_PWD = 'justsomepwd'

    BASE_URL = getenv('PIXELA_BASE_URL')

    GRPH_COLOR = 'kuro'
    GRPH_ID = 'codegraph'

    main()
