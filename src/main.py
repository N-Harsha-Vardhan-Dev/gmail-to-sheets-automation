from src.gmail_service import GmailService
from src.sheets_service import SheetsService
from src.email_parser import parse_email


def main():
    print("Initializing services...")
    
    gmail = GmailService()
    sheets = SheetsService()

    print("Fetching unread emails...")
    unread_messages = gmail.fetch_unread_emails()

    if not unread_messages:
        print("No unread emails found. Exiting.")
        return

    print(f"{len(unread_messages)} unread emails found.")

    processed_count = 0

    for msg in unread_messages:  # Limit to first 10 for testing
        msg_id = msg["id"]

        # Get full email content
        raw_email = gmail.get_email(msg_id)

        # Parse into clean fields
        parsed = parse_email(raw_email)

        # Prepare row for Google Sheets
        row = [
            parsed["from"],
            parsed["subject"],
            parsed["date"],
            parsed["content"]
        ]

        # Append to sheet
        sheets.append_row(row)

        # Mark email as read
        gmail.mark_as_read(msg_id)

        processed_count += 1

    print(f"Completed. {processed_count} emails appended to Google Sheets.")


if __name__ == "__main__":
    main()
