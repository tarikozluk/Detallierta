import requests
import os
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("CITRIX_USER")
password = os.getenv("CITRIX_PASSWORD")


url = 'https://'+os.getenv("CITRIX_URL")+'/nitro/v1/config/server'
response = requests.get(url, auth=(user, password), verify=False)
data = response.json()
print(data)


#todo: enabled and disabled servers will be added to elasticsearch to save history