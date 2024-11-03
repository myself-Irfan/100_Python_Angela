import logging
import os
import requests
from dotenv import load_dotenv
import geocoder


class RainInfoModule:
    def __init__(self):
        logging.info('Initializing')

        self.lat = None
        self.long = None

        self.__get_cur_co_ord()

    def __get_cur_co_ord(self):
        logging.info(f'Initiating')

        try:
            g = geocoder.ip('me')
            if g.ok and g.latlng:
                self.lat, self.long = g.latlng
                logging.info(f'Co ordinates set: ({self.lat}, {self.long})')
            else:
                logging.warning(f'Failed to obtain co-ordinates | g.ok={g.ok}, g.latlng={g.latlng}, g.status={g.status or "unknown"}, ')
        except Exception as e:
            logging.error(f'Unexpected Error: {e}')


    def __make_req(self):
        logging.info(f'Initiating')

        header = {
            'lat': self.lat,
            'lon': self.long,
            'appid': API_KEY,
            'cnt': RESP_COUNT
        }

        try:
            w_resp = requests.get(url=API_URL, params=header, timeout=TIMEOUT_MS)
            w_resp.raise_for_status()
            return w_resp.json().get('list')
        except requests.exceptions.HTTPError as http_err:
            logging.error(f'HTTP Error: {http_err}')
        except requests.exceptions.ConnectionError as conn_err:
            logging.error(f'Connection Error: {conn_err}')
        except requests.exceptions.Timeout as timeout_err:
            logging.error(f'Timeout Error: {timeout_err}')
        except requests.exceptions.RequestException as req_err:
            logging.error(f'Request Error: {req_err}')
        except Exception as e:
            logging.error(f'Unexpected Error: {e}')

        return None


    def __clean_data(self) -> list[int]:
        resp = self.__make_req()

        return [r.get('weather')[0].get('id') for r in resp]

    def return_verdict(self) -> str:
        weather_codes = self.__clean_data()
        logging.debug(f'Weather Codes: {weather_codes}')

        for w_code in weather_codes:
            if w_code < 700:
                return 'Advising to take an umbrella as a caution'

        return 'No rain expected. Enjoy the sun!'

def main():
    i_rain = RainInfoModule()
    print(i_rain.return_verdict())


if __name__ == '__main__':
    load_dotenv()

    cur_f_name = os.path.basename(__file__)
    cur_f_name = os.path.splitext(cur_f_name)[0]

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s -> %(funcName)s | %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f'{cur_f_name}.log')
        ]
    )

    API_URL = os.getenv('OPENWEATHER_URL')
    API_KEY = os.getenv('OPENWEATHER_KEY')
    TIMEOUT_MS = int(os.getenv('TIMEOUT_MS'))
    RESP_COUNT = 4

    main()