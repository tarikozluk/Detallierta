import requests
import os
from dotenv import load_dotenv
from re import search
load_dotenv()
user = os.getenv("CITRIX_USER")
password = os.getenv("CITRIX_PASSWORD")


def lb_name_finder(lb_regex):
    try:
        for i in range(1, 3):
            url = 'https://'+os.getenv("CITRIX_URL_{}".format(str(i)))+'/nitro/v1/config/lbvserver' #this part must be a variable
            response = requests.get(url, auth=(user, password), verify=False)
            lb_content = response.json()
            #print(lb_content)
            for lbs in range(len(lb_content['lbvserver'])):
                #print(lb_content['lbvserver'][lbs]['name'])
                if search(lb_regex, lb_content['lbvserver'][lbs]['name']):
                    print("found")

                    lb_full_name = lb_content['lbvserver'][lbs]['name']
                    return lb_full_name
    except:
        print("Bu lbye ait bir şey bulunamadı")


