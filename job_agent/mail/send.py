import base64, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

GMAIL_SCOPE = ["https://www.googleapis.com/auth/gmail.send"]

def _service():
    # Expects token.json at project root (OAuth user creds)
    creds = Credentials.from_authorized_user_file("token.json", GMAIL_SCOPE)
    return build("gmail", "v1", credentials=creds)

def send_email(to, subject, body, attachments=None, from_email=None):
    service = _service()
    msg = MIMEMultipart()
    msg["To"] = to
    if from_email:
        msg["From"] = from_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    for path in (attachments or []):
        with open(path, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(path))
            part["Content-Disposition"] = f'attachment; filename="{os.path.basename(path)}"'
            msg.attach(part)
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    service.users().messages().send(userId="me", body={"raw": raw}).execute()