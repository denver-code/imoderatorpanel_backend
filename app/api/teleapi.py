import requests
from app.api.config_api import *

API_TOKEN = get_value("API_TOKEN", filep="deploy_bot_config")
CHAT_ID = get_value("CHAT_ID", filep="deploy_bot_config")

def send_message(message):#&parse_mode=Markdown
    url_req = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url_req)