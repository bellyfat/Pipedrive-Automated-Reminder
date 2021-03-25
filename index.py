import functions
import mailer
import os
from dotenv import load_dotenv
load_dotenv

def two_week_check():

    # Retrieving almost finished subscriptions
    #pipeline_id = functions.get_pipeline_id()
    #stage_id = functions.get_stage_id(pipeline_id)
    #pipeline_deals = functions.get_pipeline_deals(pipeline_id)
    #subscribed_deals = functions.filter_subscribed_deals(pipeline_deals, stage_id)
    #almost_finished_subscriptions = functions.filter_almost_finished_subscriptions(subscribed_deals)
    almost_finished_subscriptions = [
        {
        "title": "This is a test subscription that finishes in 2 weeks"
        },
        {
        "title": "This is a test subscription that finishes in 2 weeks"
        },
        {
        "title": "This is a test subscription that finishes in 2 weeks"
        },
        {
        "title": "This is a test subscription that finishes in 2 weeks"
        },
        {
        "title": "This is a test subscription that finishes in 2 weeks"
        }
    ]

    # Sending emails (if any)
    if len(almost_finished_subscriptions) > 0:
        
        # Creating Mailer
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        host = os.getenv("HOST")
        port = os.getenv("PORT")
        mail_handler = mailer.Mailer(sender_email, sender_password, host, port)

        # Sending email
        subejct = 'Subscriptions finishing in 2 weeks'
        mail_parts = mail_handler.build_almost_finished_subscriptions_two_week_notification_mail_parts(almost_finished_subscriptions)
        recipients = ['n.winspear@leadership.ac.nz', 's.thomas@leadership.ac.nz', 'd.rosenthal@leadership.ac.nz']
        mail_handler_response = mail_handler.send_emails(mail_parts, subejct, recipients)

    return mail_handler_response


def main():
    response = two_week_check()
    print(response)
    

main()