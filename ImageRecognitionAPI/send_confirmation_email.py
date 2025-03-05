from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import os
load_dotenv()
# Replace with your SendGrid API key
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

def send_confirmation_email(email):
    message = Mail(
        from_email="no-reply@yourdomain.com",  # Replace with a verified email
        to_emails=email,
        subject="Welcome to Image Recognition API!",
        html_content="<strong>Thank you for signing up!</strong>"
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent to {email}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Test the function
send_confirmation_email("recipient@example.com")  # Replace with a real email address