import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from config import SCOPES, SHEET_ID, SHEET_RANGE


class SheetsService:
    def __init__(self):
        """
        Initialize Google Sheets API client using saved OAuth token.
        """
        creds = Credentials.from_authorized_user_file(
            "credentials/token.json",
            SCOPES
        )

        self.service = build("sheets", "v4", credentials=creds)

    def append_row(self, row):
        """
        Append a single row to Google Sheet.
        Row must be a list, e.g.:
        ["sender@gmail.com", "Subject", "Date", "Body"]
        """

        body = {"values": [row]}

        self.service.spreadsheets().values().append(
            spreadsheetId=SHEET_ID,
            range=SHEET_RANGE,
            valueInputOption="RAW",
            body=body
        ).execute()
