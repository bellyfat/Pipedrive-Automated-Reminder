import os
import requests
import datetime
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

def filter_almost_finished_subscriptions(subscribed_deals: list) -> list:
    almost_finished_subscriptions = []
    for deal in subscribed_deals:
        subscription_request_uri = build_request_uri(f'/subscriptions/find/{deal["id"]}')
        subscription_response = requests.get(subscription_request_uri)
        if subscription_response.status_code == 200:
            end_date = datetime.datetime.strptime(subscription_response.json()["data"]["start_date"], "%Y-%m-%d") + datetime.timedelta(days=365)
            current_date = datetime.datetime.now()
            day_count_difference = (end_date - current_date).days
            if day_count_difference <= 14:
                almost_finished_subscriptions.append(deal)
    return almost_finished_subscriptions