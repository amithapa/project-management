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