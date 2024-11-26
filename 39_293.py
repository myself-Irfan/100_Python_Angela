import logging
import os.path
from dotenv import load_dotenv
from google_sheet import GSheetService
import requests
import pandas as pd
from datetime import datetime, timedelta
from mail_service import MailService

class AmadeusService:
    def __init__(self):
        self._base_url = os.getenv('AMADEUS_API_URL')
        self._api_secret = os.getenv('AMADEUS_API_SECRET')
        self._api_key = os.getenv('AMADEUS_API_KEY')
        self._timeout = int(os.getenv('TIMEOUT_MS', 5000))

    def get_token(self):
        token_url = self._base_url + '/v1/security/oauth2/token'

        header = {
            'content-type': 'application/x-www-form-urlencoded'
        }

        params = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }

        try:
            resp = requests.post(url=token_url, data=params, headers=header, timeout=self._timeout)
            resp.raise_for_status()
            return resp.json().get('access_token')
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
        return {}

    def search_city(self, bearer_token: str, city_name: str):
        city_url = self._base_url + '/v1/reference-data/locations/cities'

        header = {
            'Authorization': f'Bearer {bearer_token}'
        }

        query = {
            'keyword': city_name,
            'max': 1
        }

        try:
            resp = requests.get(url=city_url, headers=header, params=query)
            resp.raise_for_status()
            return resp.json().get('data')
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
        return {}

    def get_offer(self, bearer_token: str, destination_loc: str, travel_dt: str):
        offer_url = self._base_url + '/v2/shopping/flight-offers'

        headers = {
            'Authorization': f'Bearer {bearer_token}'
        }

        query = {
            'originLocationCode': ORIGIN_AIRPORT,
            'destinationLocationCode': destination_loc,
            'departureDate': travel_dt,
            'adults': 1,
            "nonStop": "true",
            "currencyCode": "CAD",
            'max': 1
        }

        try:
            resp = requests.get(url=offer_url, headers=headers, params=query, timeout=self._timeout)
            resp.raise_for_status()
            return resp.json().get('data')
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
        return {}


def make_travel_dt(days_interval: int = 30) -> str:
    travel_dt = datetime.now() + timedelta(days=days_interval)
    travel_dt = travel_dt.strftime('%Y-%m-%d')
    logging.debug(f'Travel Date is {travel_dt}')
    return travel_dt


def main():
    i_sheet = GSheetService()
    i_amadeus = AmadeusService()
    i_mail = MailService()

    sheet_data = i_sheet.fetch_data()
    header, *rows = sheet_data
    df = pd.DataFrame(data=rows, columns=header)

    api_token = i_amadeus.get_token()
    logging.debug(f'Token: {api_token}')

    # for index, row in df.iterrows():
    #     json_resp = i_amadeus.search_city(api_token, row.get('City'))
    #     try:
    #         if json_resp:
    #             row['IATA Code'] = json_resp[0].get('iataCode', 'n/a')
    #             row['State Code'] = json_resp[0].get('address').get('stateCode', 'n/a')
    #         else:
    #             logging.warning('Response empty')
    #             row['IATA Code'] = 'n/a'
    #             row['State Code'] = 'n/a'
    #     except Exception as err:
    #         logging.error(f'Unexpected Error: {err}')
    #         row['IATA Code'] = 'n/a'
    #         row['State Code'] = 'n/a'


    # """
    # df.values.tolist -> converts a list of lists of str
    # df.columns.tolist() -> list of str
    # """
    # df_li = [df.columns.tolist()] + df.values.tolist()
    # # df_li = [list(df.columns)] + df.to_numpy().tolist()
    # i_sheet.paste_data(data=df_li)

    travel_dt = make_travel_dt()
    for index, row in df.iterrows():
        json_resp = i_amadeus.get_offer(api_token, row.get('IATA Code'), travel_dt)
        logging.info(json_resp)
        try:
            if json_resp:
                row['Price'] = json_resp[0].get('price').get('total', 'n/a')
            else:
                logging.warning("Response is empty")
                row['Price'] = 'n/a'
        except Exception as err:
            logging.error(f'Unexpected Error: {err}')
            row['Price'] = 'n/a'


    df_li = [df.columns.tolist()] + df.values.tolist()
    i_sheet.paste_data(data=df_li)

    customer_sheet = i_sheet.fetch_data('customers')[1:]
    customer_li = [customer[1] for customer in customer_sheet]

    i_mail.send_mail(customer_li, f'{cur_f_name} Test', 'https://docs.google.com/spreadsheets/d/1oG1wXoCQRSSfRr1XoxlQSVZtlkzS9mC5X-mwrXtav8c')

    logging.info(f'Customer List: {customer_li}')

    logging.info('Execution complete')

if __name__ == '__main__':
    cur_f_name = os.path.splitext(os.path.basename(__file__))[0]

    load_dotenv()

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s | %(funcName)s -> %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f'{cur_f_name}.log')
        ]
    )

    ORIGIN_AIRPORT = 'LON'

    main()
