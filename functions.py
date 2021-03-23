import os
from dotenv import load_dotenv
load_dotenv()

API_TOKEN: str = os.getenv("API_TOKEN")
COMPANY_DOMAIN: str = os.getenv("COMPANY_DOMAIN")

def build_request_uri(endpoint: str, query_params:list = []) -> str:
    params_string = "&".join(query_params) if len(query_params) > 0 else ""
    return f"https://{COMPANY_DOMAIN}.pipedrive.com/v1{endpoint}?{params_string}&api_token={API_TOKEN}"

