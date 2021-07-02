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

GFSAPI_HOST = "192.168.56.60" # "192.168.0.160"
GFSAPI_PORT = '5000'

STATUS_FAILING = "FAILING"
STATUS_UP_SYNCRONIZED = "UP"
STATUS_PENDING_UPDATE = "PENDING"
STATUS_LAGGING_UPDATE = "LAGGING"

AGENT_ID="NODE_AGENT"
PROXMOX_NODE_TYPE="ProxmoxNode"

PROXMOX_NODE_STATUS_ENDPOINT = PROXMOX_API + "/api2/extjs/nodes/{proxmox_node}/status"
PROXMOX_QEMU_ENDPOINT = PROXMOX_API + "/api2/extjs/nodes/{proxmox_node}/qemu"
PROXMOX_QEMU_CONFIG_ENDPOINT = PROXMOX_API + "/api2/extjs/nodes/{proxmox_node}/qemu/{vmid}/config"

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

#########################################################
# 🔆 🔆 🔆 🔆    Impls     🔆 🔆 🔆 🔆
#########################################################

def get_proxmox_request(proxmox_url):
    # print ("requesting: " + proxmox_url)
    response = requests.get (
        url=proxmox_url, 
        headers=headers,
        verify=False)
    retval_obj = dict(json.loads(response.text))
    # print (retval_obj)

    retval = retval_obj['data']
    # print ('---------')
    # print (retval)
    return (response.status_code, retval) 

# This is to handle adding a proxmox server to the graph
def sync_new_VMs(statedata):
    vms = get_proxmox_request(PROXMOX_QEMU_ENDPOINT.format(proxmox_node = statedata['data']['name']))
    for vm in vms[1]:
        vm_id = vm['vmid']
        vm_name = vm['name']
        vmname_composite = vm_id + " (" + vm_name + ")"
        proxmox_id = statedata['id']
        proxmox_node = statedata['data']['name']

        vm_config = dict(get_proxmox_request(PROXMOX_QEMU_CONFIG_ENDPOINT.format(
            proxmox_node = proxmox_node, 
            vmid = vm_id))[1]
        )
        resources = "ProxmoxVMTemplates" if 'template' in vm_config else 'ProxmoxVMs'
        resource = "ProxmoxVMTemplate" if 'template' in vm_config else 'ProxmoxVM'

        # print (resource)
        print ('')
        print ("  🖥️  " + (str(vm['vmid'])) + " (" + str(vm_config.get('name', {})) + ")")
        # print ("     " + str(vm_config))
 
        vm_gfs = gfs_gqlclient.gqlexec("""
            query getVM($vmId:String!, $proxmoxNode:String!) {
            """ + resources + """ (
                vmId : $vmId,
                HostedOn: {
                    name: $proxmoxNode
                }
            ) {
                id,
                name,
                HostedOn {
                id,
                name
                }
            }
            }
            """,
            {
                "vmId": vm_id,
                "proxmoxNode": proxmox_node
            }
        )['data'][resources]
        # print ("VM query result: " + str(vm_gfs) + " len(vm_gfs): " + str(len(vm_gfs)))
        # print ("vmId: " + vm_id + "   proxmoxNode: " + proxmox_node)
        # return

        # create the VM if it wasn't found. 
        ##  @TODO - createOrUpdate behavior
        if (len(vm_gfs) == 0):
            print ("     Didn't find VM [ " +  vm_id + "] in GFS on " + proxmox_node + ", creating minimal " + resource)
            print 
            if ('template' in vm_config):
                createVM = gfs_gqlclient.gqlexec("""
                    mutation createProxmoxVMTemplate($vmID:String!, $name:String!, $vmName: String!, $hostedOn:String, $template:String!, $status:String) {
                        create""" + resource + """ (
                            vmId: $vmID
                            name: $name,
                            vmName: $vmName,
                            setHostedOn: {
                                id: $hostedOn
                            },
                            template: $template,
                            status: $status
                        ) {
                            ok,
                            error,
                            instance {
                                id,
                                HostedOn {
                                    id
                                }
                            }
                        }
                    }
                """,
                    {
                        "name": vmname_composite,
                        "vmID": vm_id,
                        "vmName": vm_name,
                        "hostedOn": proxmox_id,
                        "template": "1",
                        "status": STATUS_PENDING_UPDATE
                    }
                )
            else:
                createVM = gfs_gqlclient.gqlexec("""
                    mutation createProxmoxVM($vmID:String!, $name:String!, $vmName: String!, $hostedOn:String, $status:String) {
                        create""" + resource + """ (
                            vmId: $vmID
                            name: $name,
                            vmName: $vmName,
                            setHostedOn: {
                                id: $hostedOn
                            },
                            status: $status
                        ) {
                            ok,
                            error,
                            instance {
                                id,
                                HostedOn {
                                    id
                                }
                            }
                        }
                    }
                """,
                    {
                        "name": vmname_composite,
                        "vmID": vm_id,
                        "vmName": vm_name,                        
                        "hostedOn": proxmox_id,
                        "status": STATUS_PENDING_UPDATE
                    }
                )
            print ('     Created ' + vm_id + ' [ ' + resource + '] in GFS on [ ' + proxmox_node + " ]")
            # print ('          ' + str(createVM))
        else: 
            print ('     Skipping creation of ' +   vm_id + ' [ ' + resource + '] - Found in GFS HostedOn [ ' + proxmox_node + ' ] . ')
    return

def sync_proxmox_node(statedata): 
    # print (statedata)

    # @TODO - fix the platform so update loops don't happen, only pulse-like
    #   scenarios happen. 
    id = statedata['id']
    proxmox_node = statedata['data']['name']
    label = statedata['label']

    if (label != PROXMOX_NODE_TYPE):
        print ('Not handling event for label: ' + label + '  [ id: ' + id + ' ]')
        return

    print ('Event: 🟠  ' + proxmox_node + ' [' + PROXMOX_NODE_TYPE + ']')

    gfs_node = gfs_gqlclient.gqlget(
        resource=PROXMOX_NODE_TYPE,
        arguments={
            "id": "String!",
        },
        variables={
            "id": id,
        },
        fields=[
            'id',
            'name',
            'status',
            'lastStatusModifiedTime',
            'lastAgentUpdateID'
        ]
    )
    # print (gfs_node)
    if (gfs_node['lastAgentUpdateID'] == AGENT_ID):
        print ('found lastAgentUpdateID as this agent, returning from event: ' + str(statedata['description']))
        return False

    node = get_proxmox_request(PROXMOX_NODE_STATUS_ENDPOINT.format(
            proxmox_node = proxmox_node
        ))
    if (node[0] != 200):
        print ("node doesn't exist in proxmox via " + PROXMOX_NODE_STATUS_ENDPOINT.format(proxmox_node = statedata['data']['name']) + " - @TODO - set the node to MODEL_ERROR (or something).")
    # print ("node: " + str(node[1]))

    gfs_node = gfs_gqlclient.gqlupdate(
        resource=PROXMOX_NODE_TYPE,
        arguments={
            "id": "String!",
            "cpuinfo": "String",
            "cpu" : "String",
            "memory" : "String",
            "swap" : "String",
            "uptime" : "String",
            "loadavg" : "String",
            "idle" : "String",
            "wait" : "String",
            "ksm" : "String",
            "rootfs" : "String",
            "kversion" : "String",
            "pveversion" : "String",
            "status" : "String",
            "lastStatusModifiedTime" : "Int",
            "lastAgentUpdateID" : "String",
        },
        variables={
            "id": statedata['id'],
            "cpuinfo": str(node[1]['cpuinfo']),
            "cpu": str(node[1]['swap']),
            "memory": str(node[1]['memory']),
            "swap": str(node[1]['swap']),
            "uptime": str(node[1]['uptime']),
            "loadavg": str(node[1]['loadavg']),
            "idle": str(node[1]['idle']),
            "wait": str(node[1]['wait']),
            "ksm": str(node[1]['ksm']),
            "rootfs": str(node[1]['rootfs']),
            "kversion": str(node[1]['kversion']),
            "pveversion": str(node[1]['pveversion']),
            "status": STATUS_UP_SYNCRONIZED,
            "lastStatusModifiedTime": current_sec_time(),
            "lastAgentUpdateID": AGENT_ID
        },
        fields=[
            'name',
            'status',
            'lastStatusModifiedTime'
        ]
    )
    return True

#########################################################
# 🔆 🔆 🔆 🔆    Handlers     🔆 🔆 🔆 🔆
#########################################################

def create_handler(statedata):
    print ("")
    print ("---------Create Handler----------------")
    sync_proxmox_node(statedata)
    sync_new_VMs(statedata)

def update_handler(statedata):
    print ("")
    print ("---------Update Handler----------------")
    if (sync_proxmox_node(statedata)):
        sync_new_VMs(statedata)

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
    # endpoint = PROXMOX_QEMU_ENDPOINT.format (
    #     proxmox_node = PROXMOX_NODE
    # )
    # print (endpoint)
    # response = requests.get(
    #     endpoint,
    #     headers = headers,
    #     verify = False,
    # )
    # print(response.text)
    # next_id = dict(json.loads(response.text))['data']
    # print (next_id)

    status_fields = [
            'id',
            'name',
            'status',
            'statusTimeoutSecs',
            'lastPulseModifiedTime',
            'lastStatusModifiedTime',
            'vmid'
    ]
#     vmid = '100'
#     print (vmid)
#  #   resource = "ProxmoxVMTemplates" if 'template' in vm_config else 'ProxmoxVMs'
#     resource = 'ProxmoxVMTemplates'
#     # print (resource)
#     node_gfs = gfs_gqlclient.gqlget(
#         resource=resource,
#         arguments={
#             "vmid": "String"
#         },
#         variables={
#             "vmid": vmid
#         },
#         fields=status_fields
#     )

#     print (node_gfs)

    status_fields = [
            'id',
            'name',
            'status',
            'statusTimeoutSecs',
            'lastPulseModifiedTime',
            'lastStatusModifiedTime',
    ]
    gfs_node = gfs_gqlclient.gqlupdate(
        resource="ProxmoxNode",
        arguments={
            "id": "String!",
            'status': "String",
        },
        variables={
            "id": '218',
            'status': 'testing',
        },
        fields=status_fields
    )
    print (gfs_node)


if __name__ == "__main__":
    main()





