import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()


s_id = "CYYZ"

wx_auth = os.getenv('wx_auth')

headers = {
    'Authorization': wx_auth
}

#print(f"https://avwx.rest/api/metar/{s_id}")

response = requests.get(f"https://avwx.rest/api/metar/{s_id}", headers=headers)

parse = json.dumps(response.json(), indent= 4, sort_keys= True)

print(response.status_code)