from utilities.functions import format_json
import requests

urls = "https://api.openaq.org/v3/locations/8118"
def get_api_info(url):
    url = f"{url}"
    headers = {"X-API-Key": "98684b1aef4366e1818f67d106fc5864d98ca44500b080d6a0df5b1f4ddf2a9f"}
    response = requests.get(url, headers=headers)
    print(response.content)
    
get_api_info(urls)
    