
import sys

import os
import logging
# logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)

import requests
import asyncio

import json
import time
from gfsgql import GFSGQL

from python_graphql_client import GraphqlClient

# PROXMOX_API_HOST = os.getenv('PROXMOX_API_HOST', '10.88.88.45')
# PROXMOX_API_PORT = os.getenv('PROXMOX_API_PORT', '8006')
# PROXMOX_API_TOKEN_ID = os.getenv('PROXMOX_API_TOKEN_ID', 'root@pam!integtesting')
# PROXMOX_API_TOKEN_SECRET = os.getenv('PROXMOX_API_TOKEN_SECRET', 'ad58e8e6-f1de-4d69-85c6-33bb1a635e12')
# PROXMOX_POOL=os.getenv('PROXMOX_POOL')
# PROXMOX_TARGET_HOST=os.getenv('PROXMOX_TARGET_HOST')
# PROXMOX_API = "https://" + PROXMOX_API_HOST + ":" + PROXMOX_API_PORT
# 
# gfs_ns = os.environ.get("GFS_NAMESPACE", "gfs1")
# gfs_host = os.environ.get("GFS_PUSHER_HOST", "gfsapi")
# gfs_port = os.environ.get("GFS_PUSHER_PORT", "5002")
# # gfs_username = os.environ.get("GFS_PUSHER_USERNAME", "root")
# # gfs_password = os.environ.get("GFS_PUSHER_PASSWORD", "root")
# 
# endpoint = "ws://" + str(gfs_host) + ":" + str(gfs_port) + "/" + str(gfs_ns) + "/graphql/subscriptions"
# 
# client = GraphqlClient(
#     endpoint=endpoint
# )
# 
# ignore InsecureRequestWarning: Unverified HTTPS request is being made to host ...
requests.packages.urllib3.disable_warnings() 

PROXMOX_API_HOST = os.getenv('PROXMOX_API_HOST', '10.88.88.45')
PROXMOX_API_PORT = os.getenv('PROXMOX_API_PORT', '8006')
PROXMOX_API_TOKEN_ID = os.getenv('PROXMOX_API_TOKEN_ID', 'root@pam!integtesting')
PROXMOX_API_TOKEN_SECRET = os.getenv('PROXMOX_API_TOKEN_SECRET', 'ad58e8e6-f1de-4d69-85c6-33bb1a635e12')
PROXMOX_POOL=os.getenv('PROXMOX_POOL')
PROXMOX_TARGET_HOST=os.getenv('PROXMOX_TARGET_HOST')
PROXMOX_API = "https://" + PROXMOX_API_HOST + ":" + PROXMOX_API_PORT

GFSAPI_NS = os.environ.get("GFS_NAMESPACE", "gfs1")
GFSAPI_HOST = os.getenv('GFSAPI_HOST', 'gfsapi')
GFSAPI_PORT = os.getenv('GFSAPI_PORT', '5000')

GFSWS_HOST = os.getenv('GFSWS_HOST', 'gfsapi')
GFSWS_PORT = os.getenv('GFSWS_PORT', '5002')

STATUS_FAILING = "FAILING"
STATUS_UP_SYNCRONIZED = "UP"
STATUS_PENDING_UPDATE = "PENDING"
STATUS_LAGGING_UPDATE = "LAGGING"

AGENT_ID="NODE_AGENT"
PROXMOX_NODE_TYPE="ProxmoxNode"

PROXMOX_NODE_STATUS_ENDPOINT = PROXMOX_API + "/api2/extjs/nodes/{proxmox_node}/status"
PROXMOX_QEMU_ENDPOINT = PROXMOX_API + "/api2/extjs/nodes/{proxmox_node}/qemu"
PROXMOX_QEMU_CONFIG_ENDPOINT = PROXMOX_API + "/api2/extjs/nodes/{proxmox_node}/qemu/{vmid}/config"

gfs_gqlclient = GFSGQL (
    gfs_host = GFSAPI_HOST, # gfs_host,
    gfs_port = GFSAPI_PORT, # gfs_port,
    gfs_username = None, # gfs_username,
    gfs_password = None, # gfs_password,
)

gfs_wsclient = GraphqlClient(
    endpoint="ws://" + str(GFSWS_HOST) + ":" + str(GFSWS_PORT) + "/" + str(GFSAPI_NS) + "/graphql/subscriptions"
)

## pve VM on macbook air - JMK
# headers = {
#     'user-agent': "botcanics-restclient",
#     'content-type': "application/json",
#     'authorization': "PVEAPIToken=root@pam!rootadmin=02a34aa5-44cb-4e74-9c0e-6a630cc5f5b2"
# }

headers = {
    'user-agent': "botcanics-restclient",
    'content-type': "application/json",
    'authorization': "PVEAPIToken=" + PROXMOX_API_TOKEN_ID + "=" + PROXMOX_API_TOKEN_SECRET
}

gfs_gqlclient = GFSGQL (
    gfs_host = GFSAPI_HOST, # gfs_host,
    gfs_port = GFSAPI_PORT, # gfs_port,
    gfs_username = None, # gfs_username,
    gfs_password = None, # gfs_password,
)

def current_sec_time():
    return round(time.time())

queryfile = open("./subscriber.graphql", "r")
query = queryfile.read()

def pathtostring(path):
    spath = ""
    if path:
        for pathitem in path:
            # if "label" in pathitem and "source" in pathitem and "target" in pathitem:
            spath = "(" + pathitem.get("source", {}).get("label") + " " + pathitem.get("source", {}).get("id") + " -> " + pathitem.get("label") + " -> " + pathitem.get("target", {}).get("label") + " " + pathitem.get("target", {}).get("id") + ") " + spath
    return spath

def current_sec_time():
    return round(time.time())

def load_pulsable(id, label):

    try:
        gfs_node = gfs_gqlclient.gqlget(
            resource=label, # PROXMOX_NODE_TYPE,
            arguments={
                "id": "String!",
            },
            variables={
                "id": id,
            },
            # fields=[
            #     'id',
            #     'name',
            #     'status',
            #     'lastStatusModifiedTime',
            #     'lastAgentUpdateID'
            # ],
            fields = [
                "id", 
                "name", 
                "label", 
                "status", 
                "lastStatusModifiedTime", 
                "statusTimeoutSecs", 
                "lastPulseModifiedTime", 
                "step", 
                "lastAgentUpdateID"
            ]
        )
        return gfs_node

    except Exception as e:
        return None

#########################################################
# 🔆 🔆 🔆 🔆    Impls     🔆 🔆 🔆 🔆
#########################################################

def get_proxmox_request(proxmox_url):
    # print ("requesting: " + proxmox_url)
    response = requests.get(
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
def sync_new_VMs(data):
    vms = get_proxmox_request(PROXMOX_QEMU_ENDPOINT.format(
        proxmox_node = data['data']['name'])
    )
    for vm in vms[1]:
        vm_id = vm['vmid']
        vm_name = vm['name']
        vmname_composite = vm_id + " (" + vm_name + ")"
        proxmox_id = data['id']
        proxmox_node = data['data']['name']

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
                            vmId: $vmID,
                            name: $name,
                            vmName: $vmName,
                            setHostedOn: {
                                id: $hostedOn
                            },
                            template: $template,
                            discovered: \"yes\",
                            status: $status,
                            statusTimeoutSecs: 30
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
                        "vmID": vm_id,
                        "name": vmname_composite,
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
                            vmId: $vmID,
                            name: $name,
                            vmName: $vmName,
                            setHostedOn: {
                                id: $hostedOn
                            },
                            discovered: \"yes\",
                            status: $status,
                            statusTimeoutSecs: 30
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
                        "vmID": vm_id,
                        "name": vmname_composite,
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

def sync_proxmox_node(data):
    # print (data)

    # @TODO - fix the platform so update loops don't happen, only pulse-like
    #   scenarios happen. 
    id = data['id']
    proxmox_node = data['name']
    label = data['label']

    if (label != PROXMOX_NODE_TYPE):
        print ('Not handling event for label: ' + label + '  [ id: ' + id + ' ]')
        return False

    print ('Event: 🟠  ' + proxmox_node + ' [' + PROXMOX_NODE_TYPE + ']')

    # gfs_node = data
    # print (gfs_node)
    proxmox_node = "lab1" # gfs_node.get("name") # data['data']['name']
    if (data['lastAgentUpdateID'] == AGENT_ID):
        print ('found lastAgentUpdateID as this agent, returning from event')
        return False

    node = get_proxmox_request(PROXMOX_NODE_STATUS_ENDPOINT.format(
            proxmox_node = proxmox_node
        ))
    if (node[0] != 200):
        print ("node doesn't exist in proxmox via " + PROXMOX_NODE_STATUS_ENDPOINT.format(proxmox_node = data['data']['name']) + " - @TODO - set the node to MODEL_ERROR (or something).")
    print ("node: " + str(node[1]))

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
            "id": data['id'],
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

def save_proxmox_node(data):
    # print ("")
    # print ("---------Save Node Handler----------------")
    # print (data)
    pass

def save_proxmox_vm(data):
    # print ("")
    # print ("---------Save VM Handler----------------")
    # print (data)
    pass

def save_proxmox_vmtpl(data):
    # print ("")
    # print ("---------Save VM TPL Handler----------------")
    # print (data)
    pass

def create_proxmox_node(data):
    print ("")
    print ("---------Create Node Handler----------------")
    print (data)
    print ("")

def create_proxmox_vm(data):
    print ("")
    print ("---------Create VM Handler----------------")
    print (data)
    print ("")

def create_proxmox_vmtpl(data):
    print ("")
    print ("---------Create VM TPL Handler----------------")
    print (data)
    print ("")

def update_proxmox_node(data):
    print ("---------Update Node Handler----------------")
    print (data)
    sync_proxmox_node(data)
    print ("")

def update_proxmox_vm(data):
    print ("---------Update VM Handler----------------")
    print (data)
    print ("")

def update_proxmox_vmtpl(data):
    print ("---------Update VM TPL Handler----------------")
    print (data)
    print ("")

def delete_proxmox_node(data):
    print ("---------Delete Node Handler----------------")
    print (data)
    print ("")

def delete_proxmox_vm(data):
    print ("---------Delete VM Handler----------------")
    print (data)
    print ("")

def delete_proxmox_vmtpl(data):
    print ("---------Delete proxmox_vmtpl----------------")
    print (data)
    print ("")

def callback(data = {}):

    # print(data)

    message = data.get("data", {}).get("nodeEvent", {})

    namespace = message.get('namespace', None)
    event = message.get('event', None)
    chain = message.get('chain', [])
    path = message.get('path', [])
    origin = message.get('origin', {})
    link = message.get('link', {})
    node = message.get('node', {})

    if not chain:
        chain = []

    if not path:
        path = []

    if node:

        nodeid = node.get('id', None)
        nodelabel = node.get('label', None)
        originid = origin.get('id', None)
        originlabel = origin.get('label', None)

        # logging.info(" => EVENT: namespace: " + str(namespace) + ", event: " + str(event) + ", node: " + str(nodelabel) + " " + str(nodeid) + ", origin: " + str(originlabel) + " " + str(originid) + ", path: " + str(pathtostring(path)))

        if event == "save_instance":
            if nodelabel == "ProxmoxNode":
                save_proxmox_node(load_pulsable(nodeid, nodelabel))
            elif nodelabel == "ProxmoxVM":
                save_proxmox_vm(load_pulsable(nodeid, nodelabel))
            elif nodelabel == "ProxmoxVMTemplate":
                save_proxmox_vmtpl(load_pulsable(nodeid, nodelabel))

        elif event == "create_instance":
            if nodelabel == "ProxmoxNode":
                create_proxmox_node(load_pulsable(nodeid, nodelabel))
            elif nodelabel == "ProxmoxVM":
                create_proxmox_vm(load_pulsable(nodeid, nodelabel))
            elif nodelabel == "ProxmoxVMTemplate":
                create_proxmox_vmtpl(load_pulsable(nodeid, nodelabel))

        elif event == "update_instance":
            if nodelabel == "ProxmoxNode":
                update_proxmox_node(load_pulsable(nodeid, nodelabel))
            elif nodelabel == "ProxmoxVM":
                update_proxmox_vm(load_pulsable(nodeid, nodelabel))
            elif nodelabel == "ProxmoxVMTemplate":
                update_proxmox_vmtpl(load_pulsable(nodeid, nodelabel))

        elif event == "delete_instance":
            if nodelabel == "ProxmoxNode":
                delete_proxmox_node(load_pulsable(nodeid, nodelabel))
            elif nodelabel == "ProxmoxVM":
                delete_proxmox_vm(load_pulsable(nodeid, nodelabel))
            elif nodelabel == "ProxmoxVMTemplate":
                delete_proxmox_vmtpl(load_pulsable(nodeid, nodelabel))

# Asynchronous request
loop = asyncio.get_event_loop()
loop.run_until_complete(
    gfs_wsclient.subscribe(
        query=query, 
        # handle=print
        handle=callback
    )
)
