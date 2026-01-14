import base64
from email import message_from_bytes
import re


def parse_email(email_json):
    """
    Parse a Gmail API email JSON into clean structured fields.
    Extracts:
    - sender (from)
    - subject
    - date
    - body (plain text)
    """

    payload = email_json.get("payload", {})
    headers = payload.get("headers", [])

    parsed_data = {
        "from": "",
        "subject": "",
        "date": "",
        "content": ""
    }

    # 1. Extract Headers
    for header in headers:
        name = header.get("name", "").lower()
        value = header.get("value", "")
        if name == "from":
            raw_from = value

            # Extract only the email from <email>
            match = re.search(r'<(.+?)>', raw_from)
            if match:
                parsed_data["from"] = match.group(1)  # pure email
            else:
                parsed_data["from"] = raw_from        # fallback
        elif name == "subject":
            parsed_data["subject"] = value
        elif name == "date":
            parsed_data["date"] = value

    # 2. Extract Body
    body_text = ""

    # Gmail emails often have "parts"
    parts = payload.get("parts", [])

    if parts:
        # Find a "text/plain" part (preferred)
        for part in parts:
            mime_type = part.get("mimeType", "")

            if mime_type == "text/plain":
                data = part.get("body", {}).get("data")
                if data:
                    body_text = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                    break

        # If no text/plain found → fallback to text/html
        if not body_text:
            for part in parts:
                mime_type = part.get("mimeType", "")
                if mime_type == "text/html":
                    data = part.get("body", {}).get("data")
                    if data:
                        decoded = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                        body_text = decoded  # You can convert HTML → text later
                        break

    else:
        # Simple emails have body directly in payload["body"]
        body = payload.get("body", {}).get("data")
        if body:
            body_text = base64.urlsafe_b64decode(body).decode("utf-8", errors="ignore")

    parsed_data["content"] = body_text.strip()

    return parsed_data
