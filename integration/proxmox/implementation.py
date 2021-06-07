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

headers = {
    'user-agent': "botcanics-restclient",
    'content-type': "application/json",
    'authorization': "PVEAPIToken=bots@pam!botcanics=bc1f0af3-49f1-41a2-8729-003e99ec3625"
}

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

#########################################################
# 🔆 🔆 🔆 🔆    Handlers     🔆 🔆 🔆 🔆
#########################################################

def create_handler(statedata):
    print ("----------------------------------")
    print (statedata)

def sync_proxmox(statedata):
    id = statedata['data']['id']
    typeLabel = statedata['label']

    print ("----------------------------------")
    print (statedata)

    updated_nodes = gfs_gqlclient.query(
        resource = typeLabel,
        fields = [
            "id",
            "name",
            "status",
            "lastStatusModifiedTime",
            "statusTimeoutSecs",
            "lastPulseModifiedTime",
            "proxmoxVmID"
        ]
    )
    # print (updated_nodes)

    node = None
    for node in updated_nodes:
        if (str(node['id']) == id):
            break
    # print ("id: {id} | node: {node}".format(id = id,node = node))
 
    vm_config = requests.get(
        url = PROXMOX_API + "/nodes/botcore/qemu/{proxmox_id}/config".format(
            proxmox_id = node['proxmoxVmID']),
        headers = headers,
        verify = False,
    )
    # print (vms.content)
    vm_config_dict = dict(json.loads(vm_config.content)['data'])
    # print (vm_config_dict)
 
    # clone of clone doesnt have this? Weird proxmox thing...
    # if 'machine' in vm_config_dict:
    #     print ('got here')
    #     vm_config_dict['machine'] = "not provided"
    retval = gfs_gqlclient.update(
        resource = typeLabel, 
        arguments = {
            "id": "String!", 
            "lastStatusModifiedTime": "Int",
            "net0": "String",
            "bootdisk": "String",
            "sockets": "String",
            "name": "String",
            "smbios1": "String",
            "ostype": "String",
            "template": "String",
            "cores": "String",
            "scsi0": "String",
            "memory": "String",
            "ide2": "String",
            "scsihw": "String",
            "vmgenid": "String",
            "digest": "String",
            "numa": "String",
            "machine": "String"
        },
        variables = {
            "id": id, 
            "lastStatusModifiedTime": current_sec_time(),
            "net0": vm_config_dict['net0'],
            "bootdisk": vm_config_dict['bootdisk'],
            "sockets": vm_config_dict['sockets'],
            "name": vm_config_dict['name'],
            "smbios1": vm_config_dict['smbios1'],
            "ostype": vm_config_dict['ostype'],
            "template": vm_config_dict['template'],
            "cores": vm_config_dict['cores'],
            "scsi0": vm_config_dict['scsi0'],
            "memory": vm_config_dict['memory'],
            "ide2": vm_config_dict['ide2'],
            "scsihw": vm_config_dict['scsihw'],
            "vmgenid": vm_config_dict['vmgenid'],
            "digest": vm_config_dict['digest'],
            "numa": vm_config_dict['numa'],
            "machine": vm_config_dict.get('machine', 'not provided')
        },
        fields = [
            "id",
            "lastStatusModifiedTime"
        ]
    )
    print (retval)    

def update_handler(statedata):
    _thread.start_new_thread(syncProxmox, (statedata,))
    # syncProxmox(statedata=statedata)
# print (updated_nodes)

# updated_node = requests.get(
#     url = GFSAPI_GET_NODE.format(
#         gfsid = id
#     ),
#     verify=False
# )
# print (updated_node.content)


def delete_handler(statedata):
    print ("---------Delete Handler----------------")

def link_handler(statedata):
    print ("---------Link Handler----------------")
