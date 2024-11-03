import os
from typing import Optional, Tuple
import requests
import logging
from dotenv import load_dotenv
from geopy.exc import GeopyError, GeocoderTimedOut
from geopy.geocoders import Nominatim


class ApiModule:
    def __init__(self):
        logging.info('Initializing ApiModule')

        if not ISS_API:
            logging.critical('Environment variable for API URL not set. Exiting')
            raise EnvironmentError('API URL missing')

        self.api_url = ISS_API
        self.timeout_ms = TIME_MS

    def __send_req(self):
        logging.info('Attempting to send request')

        try:
            resp = requests.get(self.api_url, timeout=self.timeout_ms)
            resp.raise_for_status()
            data = resp.json()
            return data
        except requests.exceptions.HTTPError as http_err:
            logging.error(f'HTTP Error: {http_err.response.status_code} | {http_err}')
        except requests.exceptions.ConnectionError as conn_err:
            logging.error(f'Connection Error: {conn_err}')
        except requests.exceptions.Timeout as time_err:
            logging.error(f'TImeout error: {time_err}')
        except requests.exceptions.RequestException as req_err:
            logging.error(f'Request Error: {req_err}')
        except Exception as e:
            logging.error(f'Unknown Error: {e}')

        return None

    def __clean_data(self, resp) -> Optional[Tuple[float, float]]:
        logging.info('Attempting to clean data')

        if not resp:
            logging.warning('Sending None due to response being None')
            return None

        try:
            if KEY not in resp:
                raise KeyError(f'{KEY} not found in the response')

            lat = resp.get(KEY).get('latitude')
            long = resp.get(KEY).get('longitude')
            return float(lat), float(long)
        except KeyError as k_err:
            logging.error(k_err)
        except ValueError as val_err:
            logging.error(f'Error with value: {val_err}')

        return None

    def fwd_req(self):
        return self.__clean_data(self.__send_req())


class PosModule:
    def __init__(self):
        logging.info('Initiating position module')

        self.geolocator = Nominatim(user_agent='ilocation')
        self.language = REV_LANG

    def __fetch_location(self, lat: float, long: float):
        logging.info(f'Attempting to fetch location for ({lat},{long})')

        try:
            location = self.geolocator.reverse((lat, long), exactly_one=True, language=self.language)
            logging.debug(f'Received location: {location}')
            return location.address if location else 'Location not found'
        except GeopyError as geo_err:
            logging.warning(f'Geopy error: {geo_err}')
        except GeocoderTimedOut as geoT_err:
            logging.warning(f'Geocoder Timed out: {geoT_err}')
        except Exception as e:
            logging.warning(f'Unexpected error: {e}')

        return None

    def giv_loc(self, lat: float, long: float):
        return self.__fetch_location(lat, long)


def main():
    i_api = ApiModule()
    i_pos = PosModule()

    co_ords = i_api.fwd_req()

    if co_ords:
        lat, long = co_ords
        pos = i_pos.giv_loc(lat, long)
        logging.info(f'ISS position: {pos} | {co_ords}')
    else:
        logging.warning('Failed to retrieve ISS co-ordinates')


if __name__ == '__main__':
    cur_f_name = os.path.splitext(os.path.basename(__file__))[0]

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s | %(message)s',
        handlers=[
            logging.StreamHandler(),
            # logging.FileHandler(f'{cur_f_name}.log')
        ]
    )

    load_dotenv()

    ISS_API = os.getenv('CUR_ISS_POS_API')
    TIME_MS = 5000
    KEY = 'iss_position'
    REV_LANG = 'en'

    main()