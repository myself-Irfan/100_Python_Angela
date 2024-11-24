import logging
import os
from datetime import datetime

from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build


class GSheetService:
    def __init__(self):
        self.scope = ['https://www.googleapis.com/auth/spreadsheets']
        self.service_acc_f = os.getenv('SERVICE_ACCOUNT_FILE')
        self.sheet_id = os.getenv('SHEET_ID')
        self.service = self._init_client()

    def _init_client(self):
        """
        initializes client and returns a build
        :return: resource
        """

        creds = service_account.Credentials.from_service_account_file(
            self.service_acc_f,
            scopes=self.scope
        )

        return build('sheets', 'v4', credentials=creds)

    def _get_sheet_name(self, nw_sheet: bool = False) -> str:
        """
        takes a boolean val and
        returns a string for sheet name
        :param nw_sheet: bool
        :return: str
        """
        if nw_sheet:
            return f'{datetime.now().strftime('%Y%m%d-%H%M')}'
        else:
            return f'Sheet1'

    def _create_sheet(self, sheet_name: str) -> str | None :
        """
        takes in a string
        and uses that to create a new sheet
        :param sheet_name: str
        :return: str
        """

        try:
            requests = [
                {
                    'addSheet': {
                        'properties': {
                            'title': sheet_name
                        }
                    }
                }
            ]

            body = {
                'requests': requests
            }

            response = self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.sheet_id,
                body=body
            ).execute()

            logging.info(f'Sheet {sheet_name} created successfully | {response}')
            return sheet_name

        except Exception as err:
            logging.error(f'Failed to create new sheet: {err}')
            return None

    def _get_data_range(self, data: list, sheet_name: str) -> str:
        """
        takes data to paste and sheet_name
        and returns a name w/ range for sheet
        :param data: list, sheet_name: str
        :return: str
        """

        return f'{sheet_name}!A1:{chr(ord("A") + len(data[0]) - 1)}{len(data)}'

    def paste_data(self, data: list, nw_sheet: bool = False) -> str:
        """
        takes data and sheet name
        and pastes data to specified sheet
        :params data: list, nw_sheet: bool
        :return: str
        """

        sheet_name = self._get_sheet_name(nw_sheet)

        if nw_sheet:
            self._create_sheet(sheet_name)

        sheet_range = self._get_data_range(data, sheet_name)

        body = {
            'values': data
        }

        try:
            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.sheet_id,
                range=sheet_range,
                valueInputOption='RAW',
                body=body
            ).execute()

            logging.info(f'Sheet updated: {sheet_range}')
            return f"Cells updated: {result.get('updatedCells')}"
        except Exception as e:
            logging.error(f'Failed to update sheet: {e}')
            return 'Cell update Error'


def main():
    i_sheet = GSheetService()

    data_to_paste = [
        ["Name", "Age", "City"],
        ["Alice", 30, "New York"],
        ["Bob", 25, "San Francisco"],
        ["Charlie", 35, "Chicago"]
    ]

    i_sheet.paste_data(data_to_paste)


if __name__ == '__main__':
    cur_f_name = os.path.splitext(os.path.basename(__file__))[0]

    load_dotenv()

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(funcName)s | %(message)s',
        handlers={
            logging.StreamHandler(),
            logging.FileHandler(f'{cur_f_name}.log')
        }
    )

    SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SPREADSHEET_ID = os.getenv('SHEET_ID')

    main()
