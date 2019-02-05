from credentials_base import CredentialsBase
from constants import SpreadSheetScope
from exceptions import InvalidSpreadSheetId
import gspread

class SpreadSheetServiceBase(CredentialsBase):
    def __init__(self, scope: list=[SpreadSheetScope.READONLY_SCOPES]):
        CredentialsBase.__init__(self, scope)
        self.__gs_authorize: gspread.Client = None
        self.__spreadsheet: gspread.Spreadsheet = None
        self.__selected_worksheet: gspread.Worksheet = None
        self.__setup()

    def __setup(self):
        self.__gs_authorize = gspread.authorize(self.creds)

    @property
    def spreadsheet(self):
        return self.__spreadsheet

    @property
    def selected_worksheet(self):
        return self.__selected_worksheet

    def open_spreadsheet_by_key(self, spreadsheet_key: str) -> None:
        try:
            self.__spreadsheet = self.__gs_authorize.open_by_key(spreadsheet_key)
        except gspread.exceptions.APIError as e:
            raise InvalidSpreadSheetId(f"{spreadsheet_key} is an Invalid SpreadSheet Key.")

    def open_spreadsheet_by_name(self, spreadsheet_name: str) -> None:
        try:
            self.__spreadsheet = self.__gs_authorize.open_by_key(spreadsheet_name)
        except gspread.exceptions.APIError as e:
            raise InvalidSpreadSheetId(f"{spreadsheet_name} is an Invalid Name.")

    def open_spreadsheet_by_url(self, spreadsheet_url: str) -> None:
        try:
            self.__spreadsheet = self.__gs_authorize.open_by_key(spreadsheet_url)
        except gspread.exceptions.APIError as e:
            raise InvalidSpreadSheetId(f"{spreadsheet_url} is an Invalid Url.")

    def select_spreadsheet_by_index(self, index: int) -> None:
        self.__selected_worksheet = self.spreadsheet.get_worksheet(index)

    def select_spreadsheet_by_title(self, title) -> None:
        self.__selected_worksheet = self.spreadsheet.worksheet(title)

    def get_all_worksheets(self) -> list:
        return self.spreadsheet.worksheets()

    def get_row_values_by_index(self, index: int) -> list:
        return self.__selected_worksheet.row_values(index)

    def get_col_values_by_index(self, index: int) -> list:
        return self.__selected_worksheet.col_values(index)

    def get_all_values(self) -> list:
        return self.__selected_worksheet.get_all_values()

    def create_spread_sheet(self, sheet_title: str, rows: str="100", cols: str="20"):
        self.__selected_worksheet = self.__spreadsheet.add_worksheet(title=sheet_title, rows=rows, cols=cols)

    def get_cell_by_label(self, label: str) -> gspread.models.Cell:
        return self.__selected_worksheet.acell(label)

    def get_cell_by_index(self, row: int, col: int) -> gspread.models.Cell:
        return self.__selected_worksheet.cell(row, col)

    def update_cell_by_label(self, label: str, value: str) -> None:
        self.__selected_worksheet.update_acell(label, value)
        return None

    def update_cell_by_index(self, row: int, col: int, value: str) -> None:
        self.__selected_worksheet.update_cell(row, col, value)
        return None

    def __get_range(self, startRow: int=0, endRow: int=0, startCol: int=0, endCol: int=0):
        return {
            "sheetId": self.__selected_worksheet.id,
            'startRowIndex': startRow,
            'endRowIndex': endRow,
            'startColumnIndex': startCol,
            "endColumnIndex": endCol
        }

    def apply_formatting_to_cell(self, cell_range: dict, cell: dict, fields: dict):
        """
        Refer: https://developers.google.com/sheets/api/samples/formatting
        :param cell_range:
        :param cell:
        :param fields:
        :return:
        """
        payload_data = {
            'requests': [
                {
                    'repeatCell': {
                        'range': cell_range,
                        'cell': cell,
                        'fields': fields
                    }
                }
            ]
        }
        self.__selected_worksheet.spreadsheet.batch_update(payload_data)

    def bold_range(self, startRow, endRow: int, startCol: int, endCol: int):
        cell_range = self.__get_range(startRow, endRow, startCol, endCol)
        cell = {'userEnteredFormat': {'textFormat': {'bold': True}}}
        fields = 'userEnteredFormat.textFormat.bold'
        self.apply_formatting_to_cell(cell_range, cell, fields)

