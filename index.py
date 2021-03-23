import requests
import functions

def get_pipeline_id() -> int:
    request_uri = functions.build_request_uri('/pipelines')
    all_pipelines = requests.get(request_uri).json()["data"]
    pipeline_id = list(filter(lambda pipeline : pipeline["name"] == "MyTeamPulse Subscriptions", all_pipelines))[0]["id"]
    return pipeline_id

def get_stage_id(pipeline_id: int) -> int:
    request_uri = functions.build_request_uri('/stages', [f'pipeline_id={pipeline_id}'])
    pipeline_stage_ids = requests.get(request_uri).json()["data"]
    stage_id = list(filter(lambda stage: stage["name"] == 'Subscribed', pipeline_stage_ids))[0]["id"]
    return stage_id

def get_pipeline_deals(pipeline_id: int) -> list:
    limit=50
    start=0
    request_uri = functions.build_request_uri('/deals', [f'start={start}', f'limit={limit}'])
    deal_chunk = requests.get(request_uri).json()["data"]
    pipeline_deals = list(filter(lambda deal: deal["pipeline_id"] == pipeline_id, deal_chunk))
    while len(deal_chunk) == limit:
        start += limit
        request_uri = functions.build_request_uri('/deals', [f'start={start}', f'limit={limit}'])
        deal_chunk = requests.get(request_uri).json()["data"]
        pipeline_deals += list(filter(lambda deal: deal["pipeline_id"] == pipeline_id, deal_chunk))
    return pipeline_deals

def filter_subscribed_deals(pipline_deals: list, stage_id: int) -> list:
    subscribed_deals = list(filter(lambda deal: deal["stage_id"] == stage_id, pipline_deals))
    return subscribed_deals

def main():
    pipeline_id = get_pipeline_id()
    stage_id = get_stage_id(pipeline_id)
    pipeline_deals = get_pipeline_deals(pipeline_id)
    subscribed_deals = filter_subscribed_deals(pipeline_deals, stage_id)
    print(len(subscribed_deals))

main()