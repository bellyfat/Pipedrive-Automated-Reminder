import functions
import mailer
import os
import datetime
import json
from dotenv import load_dotenv
load_dotenv

def two_week_check():

    # Retrieving almost finished subscriptions
    pipeline_id = functions.get_pipeline_id()
    stage_id = functions.get_stage_id(pipeline_id)
    pipeline_deals = functions.get_pipeline_deals(pipeline_id)
    subscribed_deals = functions.filter_subscribed_deals(pipeline_deals, stage_id)
    almost_finished_subscriptions = functions.filter_almost_finished_subscriptions(subscribed_deals)

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
        recipients = ['n.winspear@leadership.ac.nz']
        mail_handler_response = mail_handler.send_emails(mail_parts, subejct, recipients)

    else:
        mail_handler_response = {
            "message": "No messages to send."
        }

    return mail_handler_response

def create_log(response: str) -> None:
    try:
        # Setup
        log_folder_path = "/home/pi/Documents/Github/Pipedrive-Automated-Reminder/logs"
        filename = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")

        # Writing to file
        f = open("{}/{}.txt".format(log_folder_path, filename), "w")
        f.write("Check performed at: {}\n\n{}".format(
            datetime.datetime.now(), json.dumps(response.json(), indent=4, sort_keys=True)))
        f.close()
    except Exception as err:
        print("Failed to create log \n", err)

def main():
    response = two_week_check()
    create_log(response)
    

main()