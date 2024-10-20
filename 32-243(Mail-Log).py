import os
from dotenv import load_dotenv
import logging
import pytz # timezone -> Dhaka
from datetime import datetime
import requests

from smtplib import SMTP, SMTPAuthenticationError, SMTPConnectError, SMTPException
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class ApiModule:
    def __init__(self):
        self.api_url = 'https://zenquotes.io/api/today'

    def __send_req(self):
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


class MailModule:
    def __init__(self):
        load_dotenv()
        self.sender_usr = os.getenv('MAIL_APP_USR')
        self.sender_pwd = os.getenv('MAIL_APP_PWD')
        self.msg = MIMEMultipart()

    def __compose_mail(self, to_addrs, sub, body, cc_addrs=None):
        self.msg['From'] = self.sender_usr
        self.msg['To'] = to_addrs
        self.msg['Cc'] = ', '.join(cc_addrs) if cc_addrs else ''

        self.msg['Subject'] = sub
        self.msg.attach(MIMEText(body, 'plain'))

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
            logging.error(f'Failed to connect to SMTP server. Please check network connection and server settings | {e}')
            raise
        except SMTPException as e:
            logging.error(f'SMTP error occurred | {e}')
            raise
        except Exception as e:
            logging.error(f'Unknown error: {e}')
            raise

    def send_mail(self, to_addrs, sub, body, cc_addrs=None):
        self.__compose_mail(to_addrs=to_addrs, sub=sub, body=body, cc_addrs=cc_addrs)
        self.__send_mail_req(to_addrs=to_addrs, cc_addr=cc_addrs)


def main():
    iMail = MailModule()

    dhaka_tz = pytz.timezone('Asia/Dhaka')
    dhaka_now = datetime.now(dhaka_tz)
    cur_day = dhaka_now.strftime('%A').lower()  # get current day in name

    if cur_day in DAYS_2_SEND:
        logging.info(f'Today is {cur_day}. Initiating Mail!')
        sub='Holiday'
        body='Enjoy your holiday'
    else:
        logging.info(f'Today is {cur_day}. Go work!')
        iApi = ApiModule()
        sub = 'Work Day'
        body = iApi.make_request()

    iMail.send_mail(
        to_addrs=TO_USR,
        sub=sub,
        body=body
    )


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s | %(message)s',
        handlers=[
            # logging.fileHandler('mail-log.log'),
            logging.StreamHandler()
        ]
    )

    RESP_KEY = 'q'
    TIMEOUT_MS = 50

    TO_USR = 'ahmed.1995.irfan@gmail.com'
    # CC_USR = ['afzal745@gmail.com', 'irfan.ahmed@tallykhata.com']

    DAYS_2_SEND = ['friday', 'saturday']

    main()
