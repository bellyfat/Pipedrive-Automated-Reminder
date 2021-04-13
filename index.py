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
        recipients = ['n.winspear@leadership.ac.nz', 's.thomas@leadership.ac.nz', 'd.rosenthal@leadership.ac.nz']
        mail_handler_response = mail_handler.send_emails(mail_parts, subejct, recipients)

    else:
        mail_handler_response = {
            "message": "No messages to send."
        }

    #if datetime.datetime.now().day == 1:
    mail_handler_response["subscribed_deals"] = subscribed_deals

    return mail_handler_response

def create_log(response: str) -> None:
    try:
        # Setup
        log_folder_path = "/home/pi/Documents/Github/Pipedrive-Automated-Reminder/logs"
        filename = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")

        # Writing to file
        f = open("{}/{}.txt".format(log_folder_path, filename), "w")
        f.write("Check performed at: {}\n\n{}".format(
            datetime.datetime.now(), json.dumps(response, indent=4, sort_keys=True)))
        f.close()
    except Exception as err:
        print("Failed to create log \n", err)

def monthly_revenue_report(subscribed_deals: dict) -> dict:
    csv_file_path = functions.generate_subscribed_deals_data_for_monthly_revenue_report(subscribed_deals)
    
    # Creating Mailer
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    mail_handler = mailer.Mailer(sender_email, sender_password, host, port)

    # Sending email
    subejct = 'MTP Montly Revenue Report Data'
    mail_parts = mail_handler.build_mtp_data_csv_mail_parts(csv_file_path)
    recipients = ['n.winspear@leadership.ac.nz', 'd.somashekarappa@leadership.ac.nz']
    mail_handler_response = mail_handler.send_emails(mail_parts, subejct, recipients)
    return mail_handler_response

def main():
    print('Running two week check...')
    response = two_week_check()
    print('Two week check complete!')
    if response["subscribed_deals"]:
        print('Running MTP data export...')
        csv_response = monthly_revenue_report(response["subscribed_deals"])
        response["csv_response"] = csv_response
        print('MTP data export complete!')
    print('Creating log...')
    create_log(response)
    print('Log created!')


main()
