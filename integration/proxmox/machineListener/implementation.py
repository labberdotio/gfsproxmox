import requests
import json
import urllib.response
from threading import Lock, Thread
import threading
import time
import _thread

from requests.api import head
# from python_graphql_client import GraphqlClient
from gfsgql import GFSGQL

requests.packages.urllib3.disable_warnings() 

PROXMOX_HOST="192.168.0.180"
PROXMOX_PORT="8006"
PROXMOX_API= "https://" + PROXMOX_HOST + ":" + str(PROXMOX_PORT) + "/api2/json"

GFSAPI_HOST = "192.168.0.160" # "192.168.0.160"
GFSAPI_PORT = 5000

# GFSAPI = "https://" + GFSAPI_HOST + ":" + str(GFSAPI_PORT)
GFS_API = "http://" + GFSAPI_HOST + ":" + str(GFSAPI_PORT)

GFSAPI_GRAPH_NODES_URL = GFS_API + "/api/v1.0/gfs1/graph"
GFSAPI_GET_NODE = GFS_API + "/api/v1.0/gfs1/context/{gfsid}"

gfs_gqlclient = GFSGQL(
    gfs_host = GFSAPI_HOST, # gfs_host,
    gfs_port = str(GFSAPI_PORT), # gfs_port,
    gfs_username = None, # gfs_username,
    gfs_password = None, # gfs_password,
)

def current_sec_time():
    return round(time.time())

def main():
    print (gfs_gqlclient.create(
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
    ))

if __name__ == "__main__":
    main()