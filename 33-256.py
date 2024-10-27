import geocoder
import logging
import os
from dotenv import load_dotenv
import requests
from pandas.errors import EmptyDataError


class LocModule:
    def __init__(self):
        logging.info(f'Initiating {self.__class__}')
        self.timeout_ms = TIME_MS
        self.api_url = API_URL
        self.__build_api()

    def __build_api(self):
        self.lat, self.lng = self.__get_cur_co_ord()
        if self.lat and self.lng:
            logging.debug(f'Lat: {self.lat} | Long: {self.lng}')
            self.api_url = API_URL.format(self.lat, self.lng)
        else:
            logging.error('Unable to build API')
            self.api_url = None

    def __get_cur_co_ord(self):
        logging.info(f'Fetching current location co-ordinates')

        try:
            g = geocoder.ip('me')
            lat, long = g.latlng
            logging.info(f'Current lat: {lat}, long: {long}')
            return float(lat), float(long)
        except ValueError as val_err:
            logging.error(f'Value error: {val_err}')
        except Exception as e:
            logging.error(f'Error retrieving location: {e}')

        return None

    def __get_sun_info(self):
        logging.info(f'Fetching info related sun')

        if self.api_url is None:
            logging.error(f'Unable to retrieve data from {self.api_url}')
            return None

        try:
            resp = requests.get(self.api_url, timeout=self.timeout_ms)
            resp.raise_for_status()
            data = resp.json()
            return data
        except requests.exceptions.HTTPError as http_err:
            logging.error(f'HTTP Error: {http_err}')
        except requests.exceptions.ConnectionError as conn_err:
            logging.error(f'Connection error: {conn_err}')
        except requests.exceptions.Timeout as time_err:
            logging.error(f'Timeout Error: {time_err}')
        except requests.exceptions.RequestException as req_err:
            logging.error(f'Request error: {req_err}')
        except Exception as e:
            logging.error(f'Unexpected Error: {e}')

        return None

    def get_sun_data(self):
        api_data = self.__get_sun_info()

        try:
            if not api_data:
                raise EmptyDataError('Api response Empty or Null')
            elif 'results' not in api_data:
                raise KeyError(f'Key "results" not present | {api_data}')
            api_data = api_data.get('results')
            return api_data
        except KeyError as key_err:
            logging.warning(key_err)
        except EmptyDataError as empty_err:
            logging.error(empty_err)

        return None

def main():
    i_loc = LocModule()
    print(i_loc.get_sun_data())


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s | %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('33-256.log')
        ]
    )

    load_dotenv()

    API_URL = os.getenv('SUN_RISE_SET')
    TIME_MS = 5000
    REV_LANG = 'en'

    main()


