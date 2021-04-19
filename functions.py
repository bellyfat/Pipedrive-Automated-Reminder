import os
import requests
import datetime
import csv
from dotenv import load_dotenv
load_dotenv()

API_TOKEN: str = os.getenv("API_TOKEN")
COMPANY_DOMAIN: str = os.getenv("COMPANY_DOMAIN")

def build_request_uri(endpoint: str, query_params:list = []) -> str:
    params_string = "&".join(query_params) if len(query_params) > 0 else ""
    return f"https://{COMPANY_DOMAIN}.pipedrive.com/api/v1{endpoint}?{params_string}&api_token={API_TOKEN}"

def get_pipeline_id() -> int:
    request_uri = build_request_uri('/pipelines')
    all_pipelines = requests.get(request_uri).json()["data"]
    pipeline_id = list(filter(lambda pipeline : pipeline["name"] == "MyTeamPulse Subscriptions", all_pipelines))[0]["id"]
    return pipeline_id

def get_stage_id(pipeline_id: int) -> int:
    request_uri = build_request_uri('/stages', [f'pipeline_id={pipeline_id}'])
    pipeline_stage_ids = requests.get(request_uri).json()["data"]
    stage_id = list(filter(lambda stage: stage["name"] == 'Subscribed', pipeline_stage_ids))[0]["id"]
    return stage_id

def get_pipeline_deals(pipeline_id: int) -> list:
    limit=50
    start=0
    request_uri = build_request_uri('/deals', [f'start={start}', f'limit={limit}'])
    deal_chunk = requests.get(request_uri).json()["data"]
    pipeline_deals = list(filter(lambda deal: deal["pipeline_id"] == pipeline_id, deal_chunk))
    while len(deal_chunk) == limit:
        start += limit
        request_uri = build_request_uri('/deals', [f'start={start}', f'limit={limit}'])
        deal_chunk = requests.get(request_uri).json()["data"]
        pipeline_deals += list(filter(lambda deal: deal["pipeline_id"] == pipeline_id, deal_chunk))
    return pipeline_deals

def filter_subscribed_deals(pipline_deals: list, stage_id: int) -> list:
    subscribed_deals = list(filter(lambda deal: deal["stage_id"] == stage_id, pipline_deals))
    return subscribed_deals

def filter_almost_finished_subscriptions(subscribed_deals: list, weeks:int = None, days:int = None) -> list:
    filter_length = weeks * 7 if weeks else days
    almost_finished_subscriptions = []
    for deal in subscribed_deals:
        subscription_request_uri = build_request_uri(f'/subscriptions/find/{deal["id"]}')
        subscription_response = requests.get(subscription_request_uri)
        if subscription_response.status_code == 200:
            end_date = datetime.datetime.strptime(subscription_response.json()["data"]["start_date"], "%Y-%m-%d") + datetime.timedelta(days=365)
            current_date = datetime.datetime.now()
            day_count_difference = (end_date - current_date).days
            if day_count_difference == filter_length:
                almost_finished_subscriptions.append(deal)
    return almost_finished_subscriptions

##########################################################################################
#                               Deal Data Functions                                      #
##########################################################################################

def get_deal_fields(required_fields: list) -> list:
    request_uri = build_request_uri('/dealFields')
    deal_fields = requests.get(request_uri).json()["data"]
    filtered_deal_fields = []
    for deal_field in deal_fields:
        if deal_field["name"] in required_fields:
            filtered_deal_fields.append(deal_field)
    return filtered_deal_fields

def extract_deal_fields(subscribed_deals: list, deal_fields:list) -> dict:
    extracted_deal_fields = []
    for deal in subscribed_deals:
        deal_field_values = {
            "deal": deal,
        }
        for field in deal_fields:
            if deal[f"{field['key']}"]:
                for option in field["options"]:
                    if option['id'] == int(deal[f"{field['key']}"]):
                        deal_field_values[field["name"].replace(" ", "_").lower()] = option["label"]
        extracted_deal_fields.append(deal_field_values)

    return extracted_deal_fields

def write_csv_file(extracted_deal_fields: dict) -> str:
    file_name = f"/home/pi/Documents/Github/Pipedrive-Automated-Reminder/MTPExports/MTP Subscription Data | {datetime.datetime.now().date()}"
    with open(f"{file_name}.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Organisation Name', 'Deal Title', 'Annual Subscription Value', 'Client Source'])
        for extracted_deal in extracted_deal_fields:
            writer.writerow([extracted_deal["deal"]["org_name"], extracted_deal["deal"]["title"], extracted_deal["deal"]["value"], extracted_deal["client_source"]])
    return file_name

def generate_subscribed_deals_data_for_monthly_revenue_report(subscribed_deals: list) -> str:
    deal_fields = get_deal_fields(['Client Source'])
    extracted_deal_fields = extract_deal_fields(subscribed_deals, deal_fields)
    csv_file_path = write_csv_file(extracted_deal_fields)
    return csv_file_path
