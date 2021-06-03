import requests
import polling
import json
import time
from gfsgql import GFSGQL

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

GFSAPI_HOST = "192.168.0.160" # "192.168.0.160"
GFSAPI_PORT = 5000

gfs_gqlclient = GFSGQL(
    gfs_host = GFSAPI_HOST, # gfs_host,
    gfs_port = str(GFSAPI_PORT), # gfs_port,
    gfs_username = None, # gfs_username,
    gfs_password = None, # gfs_password,
)

def current_sec_time():
    return round(time.time())

def create_handler(statedata):
    print ("---------Create Handler----------------")
    print ("Machine Name: ")
    print (statedata)

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

def main():
    gfs_gqlclient.create(
        resource = "ProxmoxMachine", 
        arguments = {
            "name": "String!",
            "memory": "String",
            "sockets": "String",
            "smbios1": "String",
            "ostype": "String",
            "scsihw": "String",
            "bootdisk": "String",
            "net0": "String",
            "ide2": "String",
            "digest": "String",
            "machine": "String",
            "vmgenid": "String",
            "scsi0": "String",
            "cores": "String",
            "numa": "String",
            "lastStatusModifiedTime": "Int",
            "status": "String"
        }, 
        variables = {
            "name": "test-vm",
            "memory": "2048",
            "sockets": "1",
            "smbios1": "uuid=54a1e0ba-b062-4460-b659-f6681f2d1d35",
            "ostype": "l26",
            "scsihw": "pvscsi",
            "bootdisk": "scsi0",
            "net0": "virtio=B2:E7:CC:29:4C:7D,bridge=vmbr0,firewall=1",
            "ide2": "none,media=cdrom",
            "digest": "31e7b600d2fecc8f4953ef3cf8e72accafc40465",
            "machine": "q35",
            "vmgenid": "3c2289f7-e6d3-452c-874f-03e40825b7d8",
            "scsi0": "local-lvm-1TB:vm-102-disk-0,size=50G",
            "cores": "4",
            "numa": "0",
            "lastStatusModifiedTime": current_sec_time(),
            "status": "CREATED"
        }, 
        fields = [
            "id",
            "lastStatusModifiedTime"
        ]
    )

if __name__ == "__main__":
    main()