import requests
import polling
import json

# ignore InsecureRequestWarning: Unverified HTTPS request is being made to host ...
requests.packages.urllib3.disable_warnings() 

PMOXAPI_HOST = "192.168.0.180"
PMOXAPI_PORT = 8006
PMOXAPI = "https://" + PMOXAPI_HOST + ":" + str(PMOXAPI_PORT)
PVEAPIToken = "PVEAPIToken=bots@pam!botcanics=bc1f0af3-49f1-41a2-8729-003e99ec3625"
BASE_TEMPLATE_ID = 10000
POOL = "botcanics"
TARGET_HOST = "botcore"

PMOXAPI_NEXTID_ENDPOINT = PMOXAPI + "/api2/json/cluster/nextid"
PMOXAPI_CLONE_ENDPOINT = PMOXAPI + "/api2/extjs/nodes/botcore/qemu/{baseTemplateId}/clone?newid={nextId}&pool={pool}&name={vmName}&target={targetHost}"
PMOXAPI_STATUS_ENDPOINT = PMOXAPI + "/api2/json/nodes/botcore/qemu/{vmId}/status/current"
PMOXAPI_START_ENDPOINT = PMOXAPI + "/api2/extjs/nodes/botcore/qemu/{vmId}/status/start"
PMOXAPI_STOP_ENDPOINT = PMOXAPI + "/api2/extjs/nodes/botcore/qemu/{vmId}/status/stop"

def create_handler(statedata):
    print ("---------Create Handler----------------")
    print ("Machine Name: " + statedata["data"]["name"])

def update_handler(statedata):
    print ("---------Update Handler----------------")
    print ("Machine Name: " + statedata["data"]["name"])

def delete_handler(statedata):
    print ("---------Delete Handler----------------")
    print ("Machine Name: " + statedata["data"]["name"])

def link_handler(statedata):
    print ("---------Link Handler----------------")
    print ("Machine Name: " + statedata["data"]["name"])

### Saved Stuff for Reference
    # response = requests.get (
    #     PMOXAPI_STATUS_ENDPOINT, 
    #     headers=headers,
    #     verify=False)
    # print (response.text)