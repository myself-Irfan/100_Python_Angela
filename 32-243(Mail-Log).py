import os
import geocoder
from dotenv import load_dotenv
import logging
import pytz  # timezone -> Dhaka
from datetime import datetime
import requests

from smtplib import SMTP, SMTPAuthenticationError, SMTPConnectError, SMTPException
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class ZenModule:
    def __init__(self):
        logging.info(f'Initializing {self.__class__}')
        self.api_url = 'https://zenquotes.io/api/today'

    def __send_req(self):
        logging.info(f'Sending request from {self.__class__}')

        try:
            resp = requests.get(self.api_url, timeout=TIMEOUT_MS)
            resp.raise_for_status()
            data = resp.json()
            return data
        except requests.exceptions.HTTPError as http_err:
            logging.error(f'HTTP error: {http_err}')
        except requests.exceptions.ConnectionError as conn_err:
            logging.error(f'Connection error: {conn_err}')
        except requests.exceptions.Timeout as timeout_err:
            logging.error(f'Timeout error: {timeout_err}')
        except requests.exceptions.RequestException as req_err:
            logging.error(f'Request error: {req_err}')
        except Exception as e:
            logging.error(f'Unknown error: {e}')

    def __clean_data(self, data):
        logging.info('Cleaning response received from ZenApi')

        try:
            quote = data[0][RESP_KEY]
            return quote
        except IndexError as e:
            logging.error(f'No item in the response: {e} | {data}')
        except KeyError as e:
            logging.error(f'{RESP_KEY} key not found in response: {e} | {data}')
        except TypeError as e:
            logging.error(f'Response structure mismatch: {e} | {type(data)} -> {data}')
        except Exception as e:
            logging.error(f'Unexpected error: {e}')
        return None

    def make_request(self):
        response = self.__send_req()
        return self.__clean_data(response)


class LocModule:
    def __init__(self):
        logging.info(f'Initiating {self.__class__}')
        self.timeout_ms = TIMEOUT_MS
        self.api_url = os.getenv('SUN_RISE_SET')
        self.api_params = None
        self.__build_api()
        self.resp_req_fields = ['sunrise', 'sunset', 'solar_noon', 'day_length']

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

    def __build_api(self):
        logging.info('Building api with params')

        self.lat, self.lng = self.__get_cur_co_ord()
        if self.lat and self.lng:
            logging.debug(f'Lat: {self.lat} | Long: {self.lng}')
            self.api_params = {
                'lat': self.lat,
                'lng': self.lng,
                'tzid': 'Asia/Dhaka'
            }
        else:
            logging.error('Unable to set params')
            self.api_params = None

    def __make_get_req(self):
        logging.info(f'Fetching info related sun')

        if self.api_params is None:
            logging.error(f'Unable to retrieve data from {self.api_url}')
            return None

        try:
            resp = requests.get(self.api_url, params=self.api_params, timeout=self.timeout_ms)
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

    def __fetch_sun_data(self):
        logging.info('Cleaning data received from SunApi')
        api_data = self.__make_get_req()

        try:
            if not api_data:
                raise ValueError('Api response Empty or Null')

            if 'results' not in api_data:
                raise KeyError(f'Key "results" not present | {api_data}')

            api_data = api_data['results']

            missing_field = [field for field in self.resp_req_fields if field not in api_data]
            if missing_field:
                raise KeyError(f'Missing field in API response: {missing_field} | Response: {api_data}')

            return (
                api_data.get('sunrise'),
                api_data.get('sunset'),
                api_data.get('solar_noon'),
                api_data.get('day_length')
            )
        except KeyError as key_err:
            logging.warning(key_err)
        except ValueError as empty_err:
            logging.error(empty_err)

        return None

    def return_mail_sun(self):
        sun_data = self.__fetch_sun_data()
        if sun_data:
            sun_body = f"""
                        Today's sunrise: {sun_data[0]}, 
                        sunset: {sun_data[1]}, solar_noon: {sun_data[2]},
                        day length: {sun_data[3]}
                        """
            return sun_body
        return "Please check log for SunModule error"


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
        logging.debug(f'Response: {resp}')
        return [r.get('weather')[0].get('id') for r in resp]

    def return_verdict(self) -> str:
        weather_codes = self.__clean_data()
        logging.debug(f'Weather Codes: {weather_codes}')

        for w_code in weather_codes:
            if w_code < 700:
                return 'Advising to take an umbrella as a caution'

        return 'No rain expected. Enjoy the sun!'


class MailModule:
    def __init__(self):
        logging.info(f'Initiating {self.__class__}')
        load_dotenv()
        self.sender_usr = os.getenv('MAIL_APP_USR')
        self.sender_pwd = os.getenv('MAIL_APP_PWD')
        self.msg = MIMEMultipart()

    def __compose_mail(self, to_addrs, sub, body, cc_addrs=None):
        self.msg['From'] = self.sender_usr
        self.msg['To'] = to_addrs
        self.msg['Cc'] = ', '.join(cc_addrs) if cc_addrs else ''

        self.msg['Subject'] = sub
        self.msg.attach(MIMEText(body, 'html'))

    def __send_mail_req(self, to_addrs, cc_addr=None):
        all_recipients = to_addrs + (cc_addr if cc_addr else '')

        try:
            with SMTP('smtp.gmail.com', 587) as connection:
                connection.starttls()
                connection.login(user=self.sender_usr, password=self.sender_pwd)
                connection.sendmail(
                    from_addr=self.sender_usr,
                    to_addrs=all_recipients,
                    msg=self.msg.as_string()
                )
            logging.info(f'Mail sent to {all_recipients}')
        except SMTPAuthenticationError as e:
            logging.error(f'Failed to authenticate with SMTP server. Please check credentials | {e}')
            raise
        except SMTPConnectError as e:
            logging.error(
                f'Failed to connect to SMTP server. Please check network connection and server settings | {e}')
            raise
        except SMTPException as e:
            logging.error(f'SMTP error occurred | {e}')
            raise
        except Exception as e:
            logging.error(f'Unknown error: {e}')
            raise

    def send_mail(self, to_addrs, sub, body, cc_addrs=None):
        body = 'Dear Valued Receiver' + '<br>' + body + '<br>' + f'Best Regards, <br>Irfan Ahmed<br>{datetime.now(pytz.timezone('Asia/Dhaka')).strftime('%Y-%m-%d %I:%M %p')}'
        self.__compose_mail(to_addrs=to_addrs, sub=sub, body=body, cc_addrs=cc_addrs)
        self.__send_mail_req(to_addrs=to_addrs, cc_addr=cc_addrs)


def main():
    iMail = MailModule()
    iLoc = LocModule()
    iRain = RainInfoModule()

    dhaka_tz = pytz.timezone('Asia/Dhaka')
    dhaka_now = datetime.now(dhaka_tz)
    cur_day = dhaka_now.strftime('%A').lower()  # get current day in name

    if cur_day in DAYS_2_SEND:
        logging.info(f'Today is {cur_day}. Initiating Mail!')
        sub = 'Holiday'
        body = str(iLoc.return_mail_sun()) + '<br>' + 'Enjoy your holiday' + '<br>' + iRain.return_verdict()
    else:
        logging.info(f'Today is {cur_day}. Go work!')
        iApi = ZenModule()
        sub = 'Work Day'
        body = str(iLoc.return_mail_sun()) + '<br>' + iApi.make_request() + '<br>' + iRain.return_verdict()

    iMail.send_mail(
        to_addrs=TO_USR,
        sub=sub,
        body=body
    )


if __name__ == '__main__':
    cur_f_name = os.path.splitext(os.path.basename(__file__))[0]
    load_dotenv()

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s -> %(funcName)s | %(message)s',
        handlers=[
            logging.FileHandler(f'{cur_f_name}.log'),
            logging.StreamHandler()
        ]
    )

    RESP_KEY = 'q'
    REV_LANG = 'en'

    API_URL = os.getenv('OPENWEATHER_URL')
    API_KEY = os.getenv('OPENWEATHER_KEY')
    TIMEOUT_MS = int(os.getenv('TIMEOUT_MS'))
    RESP_COUNT = 4

    TO_USR = 'ahmed.1995.irfan@gmail.com'
    # CC_USR = ['afzal745@gmail.com', 'irfan.ahmed@tallykhata.com']

    DAYS_2_SEND = ['friday', 'saturday']

    main()
