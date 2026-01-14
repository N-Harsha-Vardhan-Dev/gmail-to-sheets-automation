from src.gmail_service import GmailService
from src.email_parser import parse_email

gmail = GmailService()
messages = gmail.fetch_unread_emails()
msg = gmail.get_email(messages[0]["id"])

print(parse_email(msg))



# from google_auth_oauthlib.flow import InstalledAppFlow
# from config import SCOPES

# flow = InstalledAppFlow.from_client_secrets_file(
#     "credentials/credentials.json",
#     SCOPES
# )

# creds = flow.run_local_server(port=0)
# print("OAuth Successful!")
