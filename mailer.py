import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Mailer:

    def __init__(self, sender_email:str, sender_password:str, host:str, port: int) -> None:
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.host = host
        self.port = port

    def send_emails(message: str) -> dict:

        return

    def build_almost_finished_subscriptions_two_week_notification_mail_parts(almost_finished_subscriptions:list) -> list:

        subscription_titles = [subscription["title"] for subscription in almost_finished_subscriptions]
        
        # Building the text part

        email_content = "\n".join(subscription_titles)

        text_part = f"""\
            Good morning!
            
            The following MyTeamPulse subscriptions are up for renewal in the next 2 weeks,
            might be a good time to reach out and see how they're getting on.

            {email_content}

            This message was send by Nathan's automated MTP subscription reminder system.
        """

        # Building the html part
        
        email_content = ""

        for title in subscription_titles:
            code_wrapped = f"<li>{title}</li>\n"
            email_content + code_wrapped
        
        html_part = """\

        """
