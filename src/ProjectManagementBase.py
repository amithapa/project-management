from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import gspread
from ProjectManagementConstants import CREDENTIALS_URL, READ_WRITE_SCOPES

class ProjectManagementBase:
    def __init__(self, scope=READ_WRITE_SCOPES):
        self.__creds = None
        self.__scope = READ_WRITE_SCOPES
        self.__setup()

    @property
    def creds(self):
        return self.__creds

    def __setup(self):
        # Storage of the credentials
        store = file.Storage(f'{CREDENTIALS_URL}/token.json')
        self.__creds = store.get()
        if not self.__creds or self.__creds.invalid:
            flow = client.flow_from_clientsecrets(f'{CREDENTIALS_URL}/credentials.json', READ_WRITE_SCOPES)
            self.__creds = tools.run_flow(flow, store)
