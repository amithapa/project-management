import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CREDENTIALS_URL = f"{BASE_DIR}/.credentials"

class SpreadSheetScope:
    # If modifying these scopes, delete the file token.json.
    READONLY_SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    # Read and write access
    READ_WRITE_SCOPES = 'https://www.googleapis.com/auth/spreadsheets'