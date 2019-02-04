from oauth2client.service_account import ServiceAccountCredentials

from constants import CREDENTIALS_URL

class CredentialsBase:
    def __init__(self, scope):
        self.__creds = None
        self.__scope = scope
        self.__setup()

    @property
    def creds(self):
        return self.__creds

    def __setup(self):
        self.__creds = ServiceAccountCredentials.from_json_keyfile_name(f'{CREDENTIALS_URL}/credentials.json', self.__scope)

