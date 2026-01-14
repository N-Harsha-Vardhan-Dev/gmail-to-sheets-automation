import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from config import SCOPES, LAST_HISTORY_FILE


class GmailService:
    def __init__(self):
        """
        Initialize Gmail API client with OAuth token handling.
        """
        creds = None
        token_path = "credentials/token.json"

        # Load existing token if available
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        # If no valid token -> trigger OAuth login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials/credentials.json",
                    SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save new token
            with open(token_path, "w") as token:
                token.write(creds.to_json())

        self.service = build("gmail", "v1", credentials=creds)

    # STATE MANAGEMENT

    def load_last_history(self):
        """
        Load last processed history ID from file.
        """
        if not os.path.exists(LAST_HISTORY_FILE):
            return None
        return open(LAST_HISTORY_FILE).read().strip()

    def save_last_history(self, history_id):
        """
        Save last processed Gmail history ID to file.
        """
        with open(LAST_HISTORY_FILE, "w") as f:
            f.write(str(history_id))

    # EMAIL OPERATIONS

    def fetch_unread_emails(self):
        """
        Fetch unread emails from INBOX.
        Returns a list of message metadata dicts (only IDs).
        """
        results = self.service.users().messages().list(
            userId="me",
            labelIds=["INBOX", "UNREAD"]
        ).execute()

        return results.get("messages", [])

    def get_email(self, msg_id):
        """
        Fetch full email content by ID.
        """
        return self.service.users().messages().get(
            userId="me",
            id=msg_id,
            format="full"
        ).execute()

    def mark_as_read(self, msg_id):
        """
        Remove UNREAD label.
        """
        self.service.users().messages().modify(
            userId="me",
            id=msg_id,
            body={"removeLabelIds": ["UNREAD"]}
        ).execute()
