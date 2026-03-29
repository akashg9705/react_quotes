
import smtplib
import os
from email.mime.text import MIMEText
import time
from backend.db import get_active_subscribers
from backend.quotes import get_quote

def send_email(to_email, quote, author):
    sender = os.environ["EMAIL_USER"]
    password = os.environ["EMAIL_PASS"]

    html = f"""
    <html>
    <body style="font-family: Arial; text-align:center;">
        <h2>✨ Daily Quote</h2>
        <p style="font-size:18px;">"{quote}"</p>
        <p><b>— {author}</b></p>
        <hr>
        <small>If you wish to unsubscribe, use the app.</small>
    </body>
    </html>
    """

    msg = MIMEText(html, "html")
    msg["Subject"] = "✨ Your Daily Quote"
    msg["From"] = sender
    msg["To"] = to_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)

def main():
    quote, author = get_quote()
    emails = get_active_subscribers()

    for email in emails:
        try:
            send_email(email, quote, author)
            print(f"Sent to {email}")
            time.sleep(2)  # prevent spam flag
        except Exception as e:
            print(f"Failed: {email} -> {e}")

if __name__ == "__main__":
    main()