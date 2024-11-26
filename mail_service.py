import logging
import os
import pytz
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP, SMTPAuthenticationError, SMTPConnectError, SMTPException
from datetime import datetime


class MailService:
    def __init__(self):
        logging.info(f'Initiating {self.__class__}')
        load_dotenv()
        self.sender_adr = os.getenv('MAIL_APP_USR')
        self.sender_pwd = os.getenv('MAIL_APP_PWD')
        self.msg = MIMEMultipart()

    def __prep_rcvr(self, rcvr_adr: list[str] = None) -> str:
        """
        can take either a string or list of string and joins them to a comma separated string
        if received None then return empty str
        :params, cc_adr: str | list
        :return: str
        """

        return ' ,'.join(rcvr_adr) if isinstance(
            rcvr_adr, list
        ) else (
            rcvr_adr if isinstance(
                rcvr_adr, str
            ) else ''
        )

    def __prep_mail(self, to_adr: list[str], sub: str, body: str, cc_adr: str = None):
        self.msg['From'] = self.sender_adr
        # preps receivers to show in headers
        self.msg['To'] = self.__prep_rcvr(to_adr)
        self.msg['Cc'] = self.__prep_rcvr(cc_adr)

        self.msg['Subject'] = sub
        self.msg.attach(MIMEText(body, 'html'))

    def __make_mail_req(self, to_adr: list[str], cc_adr: list[str] = None):
        # actual receiver data
        all_recipients = to_adr + (cc_adr or [])

        logging.debug(f'Trying to send to {all_recipients}')

        try:
            with SMTP('smtp.gmail.com', 587) as conn:
                conn.starttls()
                conn.login(user=self.sender_adr, password=self.sender_pwd)
                conn.sendmail(
                    from_addr=self.sender_adr,
                    to_addrs=all_recipients,
                    msg=self.msg.as_string()
                )
            logging.info(f'Mail successfully sent to {all_recipients}')
            return True
        except SMTPAuthenticationError as auth_err:
            logging.error(f'SMTP Authentication Error: {auth_err} | Check Credentials')
            raise
        except SMTPConnectError as conn_err:
            logging.error(f'SMTP Connection Error: {conn_err} | Check Network Connection & Server Settings')
            raise
        except SMTPException as smtp_err:
            logging.error(f'SMTP Error: {smtp_err}')
            raise
        except Exception as err:
            logging.error(f'Unexpected Error: {err}')
            raise

    def send_mail(self, to_adr: list[str], sub: str, body: str, cc_adr: list[str] = None):
        body = 'Dear Valued Receiver' + '<br>' + body + '<br>' + f'Best Regards, <br>Irfan Ahmed<br>' + datetime.now(
            pytz.timezone('Asia/Dhaka')).strftime('%Y-%m-%d %I:%M %p')
        self.__prep_mail(to_adr=to_adr, sub=sub, body=body, cc_adr=cc_adr)
        self.__make_mail_req(to_adr=to_adr, cc_adr=cc_adr)


def main():
    to_adr = ['irfan.ahmed@tallykhata.com']
    sub = f'Test from {cur_f_Name}'
    body = 'Just a placeholder'

    i_mail = MailService()
    i_mail.send_mail(to_adr, sub, body)


if __name__ == '__main__':
    cur_f_Name = os.path.splitext(os.path.basename(__file__))[0]

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s | %(funcName)s -> %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f'{cur_f_Name}.log')
        ]
    )

    main()
