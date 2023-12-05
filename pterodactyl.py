import requests

import os
#Load variables from .env file
from dotenv import load_dotenv
load_dotenv()

endpoint = os.getenv("API_ENDPOINT")
server_id = os.getenv("SERVER_ID")
api_key = os.getenv("API_KEY")


url = f"https://{endpoint}/api/client/servers/{server_id}/command"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "Accept": "Application/vnd.pterodactyl.v1+json",
}




def add_whitelist(nametag):
    #print(f"Sending request to allow {nametag}")
    data = {
    "command": f"whitelist add {nametag}",
}
    try:
        response = requests.post(url, headers=headers, json=data)
    except Exception as e:
        print(e)
        return None

    return response.status_code

def remove_whitelist(nametag):
    #print(f"Sending request to disallow {nametag}")
    data = {
    "command": f"whitelist remove {nametag}",
}
    try:
        response = requests.post(url, headers=headers, json=data)
    except Exception as e:
        print(e)
        return None

    return response.status_code

