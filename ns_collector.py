import requests
import os
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("CITRIX_USER")
password = os.getenv("CITRIX_PASSWORD")
def getServersfromNS(correct_LB):
    app_name = correct_LB
    ###nitro/v1/config/lbvserver_servicegroupmember_binding/deneme

    try:
        for i in range(1, 3):
            url = 'https://' + os.getenv("CITRIX_URL_{}".format(str(i))) + '/nitro/v1/config/lbvserver_servicegroupmember_binding/' + app_name  # this part must be a variable
            response = requests.get(url, auth=(user, password), verify=False)
            data = response.json()
            server_lists = []
            for i in range(len(data['lbvserver_servicegroupmember_binding'])):
                server_lists.append(data['lbvserver_servicegroupmember_binding'][i]['ipv46'])
            server_lists_text = ", ".join(server_lists)
            print(server_lists_text)
            return server_lists_text
    except:
        print("zort")
#todo: configure this settings to the other lb servers also and send logs to elasticsearch

#todo: after ping process is done then go directly regex filter for lb servers

#todo: after get the correct logs send message and email for the responsible person


#todo: enabled and disabled servers will be added to elasticsearch to save history