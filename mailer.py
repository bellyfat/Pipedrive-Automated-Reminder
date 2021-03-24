from email import message
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

    def send_emails(self, mail_parts: dict, subject:str, recipients:list) -> dict:

        email_response = {
            "successful": 0,
            "failed": []
        }

        with smtplib.SMTP(self.host, self.port) as mail_server:
            mail_server.ehlo()
            mail_server.starttls()
            mail_server.login(self.sender_email, self.sender_password)
        
            for recipient in recipients:

                # Build email
                email = MIMEMultipart('alternative')
                email["Subject"] = subject
                email["From"] = self.sender_email
                email["To"] = recipient

                # Attaching mail parts
                email.attach(mail_parts["text_part"])
                email.attach(mail_parts["html_part"])

                # Finalising email body
                email_body = email.as_string()

                # Sedning email
                try:
                    mail_server.sendmail(self.sender_email, recipient, email_body)
                    email_response["successful"] += 1
                except Exception as err:
                    email_response["failed"].append({"recipient": recipient, "reason": err})

        return email_response

    def build_almost_finished_subscriptions_two_week_notification_mail_parts(self, almost_finished_subscriptions:list) -> dict:

        subscription_titles = [subscription["title"] for subscription in almost_finished_subscriptions]
        
        # Building the text part

        text_subscription_titles = "\n".join(subscription_titles)

        text_part = f"""\
            Good morning!
            
            The following MyTeamPulse subscriptions are up for renewal in the next 2 weeks,
            might be a good time to reach out and see how they're getting on.

            {text_subscription_titles}

            This message was send by Nathan's automated MTP subscription reminder system.
        """

        # Building the html part
        
        html_subscription_titles_list = []

        for title in subscription_titles:
            code_wrapped = f"<li>{title}</li>"
            html_subscription_titles_list.append(code_wrapped)
           
        html_subscription_titles_string = "\n".join(html_subscription_titles_list)
        
        html_part = f"""\
            <div
                style="margin: 0 auto;font-family: Verdana; box-sizing:border-box;font-size: 14px;max-width: 850px;display: block;padding:20px;">
                <table cellpadding="0" cellspacing="0" class="main"
                    style="margin: 0;font-family: Verdana; box-sizing:border-box;font-size: 14px;background-color: #fff;border: 1px solid #e9e9e9;border-radius: 10px;border:12px solid #E0E0E0; "
                    width="100%">
                    <tbody>
                        <tr>
                            <td>
                                <img alt="" src="https://www.isldreamteam.com/tdp/images/Blank.png" style="height:10px;" /></td>
                        </tr>
                        <tr>
                            <td align="center" style="padding:5px;">
                                <img alt="SmartLeaderApps" src="https://www.isldreamteam.com/tdp/images/vibe-logo.png"
                                    width="250" /></td>
                        </tr>
                        <tr>
                            <td align="center">
                                <span style="padding-left:15px;"><b style="font-size:25px;line-height:30px;"><span
                                            style="color:#666666;">MY</span><span style="color:#5aae5a;">TEAM</span><span
                                            style="color:#666666;">PULSE&trade;</span> </b> </span></td>
                        </tr>
                        <tr style="margin: 0;font-family: Verdana;box-sizing: border-box;font-size: 14px;">
                            <td class="content-wrap"
                                style="margin: 0;font-family:Verdana; box-sizing:border-box; font-size: 14px;vertical-align: top;padding: 35px;">
                                <table cellpadding="0" cellspacing="0"
                                    style="margin: 0;font-family: Verdana;box-sizing: border-box;font-size: 14px;" width="100%">
                                    <tbody>
                                        <tr
                                            style="margin: 0;font-family: Verdana;box-sizing:border-box;font-size: 14px;width: 100%;">
                                            <td
                                                style="margin: 0em 0em 1.5em 0em;font-family: Verdana;box-sizing:border-box;font-size: 14px; text-align: center; width: 90%; color: #666666;">
                                                <p>
                                                    <strong>Good morning!</strong><br><br>
                                                    The following MyTeamPulse subscriptions are up for renewal in the next 2
                                                    weeks, might be a good time to reach out and see how they're getting on.
                                                </p>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="margin: 0;font-family:Verdana; box-sizing:border-box;font-size: 14px;
                                                line-height: 24px; vertical-align: top;padding: 0 0 20px;color:#666666; width:
                                                100%; width: 100%;">
                                                <h3>Teams to Engage</h3>
                                                <ul style="padding: 0em 2em;">
                                                    {html_subscription_titles_string}
                                                </ul>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <table
                                    style="margin: 0;font-family: Verdana;box-sizing: border-box;font-size: 14px;color: #999;"
                                    width="100%">
                                    <tbody>
                                        <tr style="margin: 0;font-family: Verdana;box-sizing:border-box;font-size: 14px;">
                                            <td style="text-align:right; padding-right:10px; border-right:3px solid #E0E0E0;">
                                                <img alt="SmartLeaderApps"
                                                    src="https://www.isldreamteam.com/tdp/images/sld-logo-grey.png"
                                                    width="180" />
                                            </td>
                                            <td
                                                style="margin:0;font-family: Verdana; box-sizing: border-box;font-size: 12px;vertical-align:top; text-align: left;color: #999; padding-left:10px;">
                                                Tel: +64 9 366 1560<br />
                                                Suite 201, Achilles House,<br />
                                                8, Commerce Street,<br />
                                                Auckland 1010<br />
                                                Website: http://www.smartleaderapps.com</td>
                                        </tr>
                                        <tr>
                                            <td colspan="2"
                                                style="margin:0;font-family: Verdana; box-sizing: border-box;font-size: 10px;vertical-align:top;padding: 20px 0;text-align: center;color: #999;">
                                                Please note, MyTeamPulse is most compatible with Google Chrome so it is
                                                recommended
                                                that it is accessed via this browser.</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        """

        text_mail_part = MIMEText(text_part, 'plain')
        html_mail_part = MIMEText(html_part, 'html')

        return {
            "text_part": text_mail_part,
            "html_part": html_mail_part
        }
