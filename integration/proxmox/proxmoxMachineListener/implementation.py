import os
import requests
import json
import time
from gfsgql import GFSGQL

# ignore InsecureRequestWarning: Unverified HTTPS request is being made to host ...
requests.packages.urllib3.disable_warnings() 

PROXMOX_API_HOST = "192.168.56.180"
PROXMOX_API_PORT = '8006'
PROXMOX_API = "https://" + PROXMOX_API_HOST + ":" + PROXMOX_API_PORT
PROXMOX_NODE="pve"

PROXMOX_API_STATUS_ENDPOINT = PROXMOX_API + "/api2/json/nodes/{proxmox_node}/qemu/{vmId}/status/current"
PROXMOX_API_START_ENDPOINT = PROXMOX_API + "/api2/extjs/nodes/{proxmox_node}/qemu/{vmId}/status/start"
PROXMOX_API_STOP_ENDPOINT = PROXMOX_API + "/api2/extjs/nodes/{proxmox_node}/qemu/{vmId}/status/stop"
PROXMOX_API_NEXTID_ENDPOINT = PROXMOX_API + "/api2/json/cluster/nextid"
PROXMOX_API_CLONE_ENDPOINT = PROXMOX_API + "/api2/extjs/nodes/{proxmox_node}/qemu/{baseTemplateId}/clone?newid={nextId}\&pool={pool}\&name={name}\&target={targetHost}"
PROXMOX_QEMU_ENDPOINT = PROXMOX_API + "/api2/extjs/nodes/{proxmox_node}/qemu"

GFSAPI_HOST = "192.168.56.60" # "192.168.0.160"
GFSAPI_PORT = '5000'

CloneOf_query = """
query getTemplateForMachine {{
  ProxmoxMachine (
    id: "{id}"
  ) {{
    id,
    name,
    CloneOf {{
      id,
      name
    }}
  }}
}}
"""

## botcore token
# PROXMOX_NODE="botcore"
# headers = {
#     'user-agent': "botcanics-restclient",
#     'content-type': "application/json",
#     'authorization': "PVEAPIToken=bots@pam!botcanics=bc1f0af3-49f1-41a2-8729-003e99ec3625"
# }

## pve VM on macbook air - JMK
PROXMOX_NODE="pve"
headers = {
    'user-agent': "botcanics-restclient",
    'content-type': "application/json",
    'authorization': "PVEAPIToken=root@pam!rootadmin=02a34aa5-44cb-4e74-9c0e-6a630cc5f5b2"
}


gfs_gqlclient = GFSGQL (
    gfs_host = GFSAPI_HOST, # gfs_host,
    gfs_port = GFSAPI_PORT, # gfs_port,
    gfs_username = None, # gfs_username,
    gfs_password = None, # gfs_password,
)

def current_sec_time():
    return round(time.time())

### Saved Stuff for Reference
    # response = requests.get (
    #     PROXMOX_API_STATUS_ENDPOINT, 
    #     headers=headers,
    #     verify=False)
    # print (response.text)

# {'event': 'create_node', 
# 'id': '98', 
# 'label': 'ProxmoxMachine', 
# 'sourceid': None, 
# 'sourcelabel': None, 
# 'targetid': None, 
# 'targetlabel': None, 
# 'chain': '', 
# 'data': {'id': '98', 'name': 'test-vm'}, 'description': 'ProxmoxMachine(98), id: 98, name: test-vm'}
# ---------Link Handler----------------
# {'event': 'create_link', 'id': '187', 'label': 'instanceOf', 'sourceid': '98', 'sourcelabel': None, 'targetid': '60', 'targetlabel': None, 'chain': '', 'data': {'id': '98', 'name': 'test-vm'}, 'description': 'ProxmoxMachine(98), id: 98, name: test-vm'}

#########################################################
# 🔆 🔆 🔆 🔆    Impls     🔆 🔆 🔆 🔆
#########################################################

def create_or_update_VM(vmid, vm_config):
    # print (vm_config)
    composite_fields = list(vm_config.keys())
    status_fields = [
            'id',
            'name',
            'status',
            'statusTimeoutSecs',
            'lastPulseModifiedTime',
            'lastStatusModifiedTime',
            'vmid'
    ]
    composite_fields.extend(status_fields)
    # print (composite_fields)
    print ("")
    print ("")
    print ("")
    print ("")

    print (vmid)
    resource = "ProxmoxVMTemplates" if 'template' in vm_config else 'ProxmoxVMs'
    # print (resource)
    node_gfs = gfs_gqlclient.gqlget(
        resource=resource,
        arguments={
            "vmid": "String"
        },
        variables={
            "vmid": vmid
        },
        fields=status_fields
    )
    print (node_gfs)

    # node_status = gfs_gqlclient.gqlget(
    #     resource=resource,
    #     arguments={
    #         "vmid": "String"
    #     },
    #     variables={
    #         "vmid": vmid
    #     },
    #     fields=composite_fields
    # )

    return
    gfs_vm = gfs_gqlclient.gqlget(
        resource="ProxmoxVMTemplate",
        arguments={
            "proxmoxVmID": "String!"
        },
        variables={
            "id": vm['']
        },
        fields=[
            'name',
            'status',
            'statusTimeoutSecs',
            'lastPulseModifiedTime',
            'lastStatusModifiedTime'
        ]
    )
    print (gfs_vm)
    return
    # vm_template = gfs_gqlclient.gqlupdate (
    #     resource="ProxmoxVMTemplate",
    #     variables= {
    #         "id": 
    # )


def create_node(node):
    print ("create_node: ")
    print (node)

def update_node(node):
    vm_config = requests.get(
        url = PROXMOX_API + "/nodes/{proxmox_node}/qemu/{proxmox_id}/config".format(
            proxmox_node = PROXMOX_NODE,
            proxmox_id = node['proxmoxVmID']),
        headers = headers,
        verify = False,
    )
    if (vm_config.status_code != 200):
        print ("node doesn't exist in proxmox, creating: " + str(node['id']))
        create_node(node)
    else: 
        print ("do update logic here for node:" + str(node['id']))

def sync_proxmox(statedata):
    id = statedata['data']['id']
    typeLabel = statedata['label']

    updated_nodes = gfs_gqlclient.query(
        resource = typeLabel,
        fields = [
            "id",
            "name",
            "status",
            "lastStatusModifiedTime",
            "statusTimeoutSecs",
            "lastPulseModifiedTime",
            "proxmoxVmID",
            "net0",
            "bootdisk",
            "sockets",
            "name",
            "smbios1",
            "ostype",
            "cores",
            "scsi0",
            "memory",
            "ide2",
            "scsihw",
            "vmgenid",
            "digest",
            "numa",
            "machine"
        ]
    )

    node = None
    print ("updated nodes:")
    for node in updated_nodes:
        print (node['name'])
        if (str(node['id']) == id):
            return update_node(node)

    return create_node(statedata)

def get_node_status(statedata):
    print ("Machine Name: " + statedata["data"]["name"])
    node_status = gfs_gqlclient.gqlget(
        resource="ProxmoxMachine",
        arguments={
            "id": "String!"
        },
        variables={
            "id": statedata['data']['id']
        },
        fields=[
            'name',
            'status',
            'statusTimeoutSecs',
            'lastPulseModifiedTime',
            'lastStatusModifiedTime'
        ]
    )
    print (node_status)
    return node_status

#########################################################
# 🔆 🔆 🔆 🔆    Handlers     🔆 🔆 🔆 🔆
#########################################################

def create_handler(statedata):
    print ("---------Create Handler----------------")
    get_node_status(statedata)
    nextid_response = requests.get (
        url=PROXMOX_API_NEXTID_ENDPOINT, 
        headers=headers,
        verify=False)
    nextid_dict = json.loads(nextid_response.text)
    next_id = nextid_dict['data']
    print (next_id)

def update_handler(statedata):
    print ("---------Update Handler----------------")
# {'event': 'update_node', 'id': '65', 'label': 'ProxmoxMachine', 'sourceid': None, 'sourcelabel': None, 'targetid': None, 'targetlabel': None, 'chain': '', 'data': {'id': '65', 'name': 'cp10001'}, 'description': 'ProxmoxMachine(65), id: 65, name: cp10001'}
    get_node_status(statedata)
    sync_proxmox(statedata)

def delete_handler(statedata):
    print ("---------Delete Handler----------------")
    print ("Machine Name: " + statedata["data"]["name"])

def link_handler(statedata):
    print ("---------Link Handler----------------")
    print (statedata)

### Saved Stuff for Reference
    # response = requests.get (
    #     PROXMOX_API_STATUS_ENDPOINT, 
    #     headers=headers,
    #     verify=False)
    # print (response.text)

def main():
    # print ("running query:")
    # print (gfs_gqlclient.create(
    #     resource = "ProxmoxMachine", 
    #     arguments = {
    #         "name": "String!",
    #         "memory": "String",
    #         "sockets": "String",
    #         "smbios1": "String",
    #         "ostype": "String",
    #         "scsihw": "String",
    #         "bootdisk": "String",
    #         "net0": "String",
    #         "ide2": "String",
    #         "digest": "String",
    #         "machine": "String",
    #         "vmgenid": "String",
    #         "scsi0": "String",
    #         "cores": "String",
    #         "numa": "String",
    #     }, 
    #     variables = {
    #         "name": "test-vm",
    #         "memory": "2048",
    #         "sockets": "1",
    #         "smbios1": "uuid=54a1e0ba-b062-4460-b659-f6681f2d1d35",
    #         "ostype": "l26",
    #         "scsihw": "pvscsi",
    #         "bootdisk": "scsi0",
    #         "net0": "virtio=B2:E7:CC:29:4C:7D,bridge=vmbr0,firewall=1",
    #         "ide2": "none,media=cdrom",
    #         "digest": "31e7b600d2fecc8f4953ef3cf8e72accafc40465",
    #         "machine": "q35",
    #         "vmgenid": "3c2289f7-e6d3-452c-874f-03e40825b7d8",
    #         "scsi0": "local-lvm-1TB:vm-102-disk-0,size=50G",
    #         "cores": "4",
    #         "numa": "0",
    #     }, 
    #     fields = [
    #         "id"
    #     ]
    # ))

    # print (
    #     gfs_gqlclient.gqlget(
    #         resource="ProxmoxMachine",
    #         arguments={
    #             "id": "String!"
    #         },
    #         variables={
    #             "id": "64"
    #         },
    #         fields=["name"]
    #     )
    # )

    # response = requests.get(
    #     PROXMOX_API_NEXTID_ENDPOINT,
    #     headers = headers,
    #     verify = False,
    # )
    # print(response.text)
    # next_id = dict(json.loads(response.text))['data']
    # print (next_id)
    endpoint = PROXMOX_QEMU_ENDPOINT.format (
        proxmox_node = PROXMOX_NODE
    )
    print (endpoint)
    response = requests.get(
        endpoint,
        headers = headers,
        verify = False,
    )
    print(response.text)
    # next_id = dict(json.loads(response.text))['data']
    # print (next_id)


if __name__ == "__main__":
    main()





