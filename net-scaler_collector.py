import requests
import os
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("CITRIX_USER")
password = os.getenv("CITRIX_PASSWORD")
app_name = "deneme"
###nitro/v1/config/lbvserver_servicegroupmember_binding/deneme
url = 'https://'+os.getenv("CITRIX_URL")+'/nitro/v1/config/lbvserver_servicegroupmember_binding/deneme' #this part must be a variable
try:
    response = requests.get(url, auth=(user, password), verify=False)
    data = response.json()
    server_lists = []
    for i in range(len(data['lbvserver_servicegroupmember_binding'])):
        server_lists.append(data['lbvserver_servicegroupmember_binding'][i]['ipv46'])
    server_lists_text = str(server_lists)
    print(server_lists_text)
except:
    print("zort")
#todo: configure this settings to the other lb servers also and send logs to elasticsearch

#todo: after ping process is done then go directly regex filter for lb servers

#todo: after get the correct logs send message and email for the responsible person


#todo: enabled and disabled servers will be added to elasticsearch to save history