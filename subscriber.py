
import sys

import os
import logging
# logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)

import asyncio

from python_graphql_client import GraphqlClient

gfs_ns = os.environ.get("GFS_NAMESPACE", "gfs1")
gfs_host = os.environ.get("GFS_PUSHER_HOST", "gfsapi")
gfs_port = os.environ.get("GFS_PUSHER_PORT", "5002")
# gfs_username = os.environ.get("GFS_PUSHER_USERNAME", "root")
# gfs_password = os.environ.get("GFS_PUSHER_PASSWORD", "root")

endpoint = "ws://" + str(gfs_host) + ":" + str(gfs_port) + "/" + str(gfs_ns) + "/graphql/subscriptions"

client = GraphqlClient(
    endpoint=endpoint
)

queryfile = open("./subscriber.graphql", "r")
query = queryfile.read()

def pathtostring(path):
    spath = ""
    if path:
        for pathitem in path:
            # if "label" in pathitem and "source" in pathitem and "target" in pathitem:
            spath = "(" + pathitem.get("source", {}).get("label") + " " + pathitem.get("source", {}).get("id") + " -> " + pathitem.get("label") + " -> " + pathitem.get("target", {}).get("label") + " " + pathitem.get("target", {}).get("id") + ") " + spath
    return spath

#########################################################
# 🔆 🔆 🔆 🔆    Handlers     🔆 🔆 🔆 🔆
#########################################################

def save_proxmox_node(statedata):
    # print ("")
    # print ("---------Save Node Handler----------------")
    # print (statedata)
    pass

def save_proxmox_vm(statedata):
    # print ("")
    # print ("---------Save VM Handler----------------")
    # print (statedata)
    pass

def save_proxmox_vmtpl(statedata):
    # print ("")
    # print ("---------Save VM TPL Handler----------------")
    # print (statedata)
    pass

def create_proxmox_node(statedata):
    print ("")
    print ("---------Create Node Handler----------------")
    print (statedata)
    print ("")

def create_proxmox_vm(statedata):
    print ("")
    print ("---------Create VM Handler----------------")
    print (statedata)
    print ("")

def create_proxmox_vmtpl(statedata):
    print ("")
    print ("---------Create VM TPL Handler----------------")
    print (statedata)
    print ("")

def update_proxmox_node(statedata):
    print ("---------Update Node Handler----------------")
    print (statedata)
    print ("")

def update_proxmox_vm(statedata):
    print ("---------Update VM Handler----------------")
    print (statedata)
    print ("")

def update_proxmox_vmtpl(statedata):
    print ("---------Update VM TPL Handler----------------")
    print (statedata)
    print ("")

def delete_proxmox_node(statedata):
    print ("---------Delete Node Handler----------------")
    print (statedata)
    print ("")

def delete_proxmox_vm(statedata):
    print ("---------Delete VM Handler----------------")
    print (statedata)
    print ("")

def delete_proxmox_vmtpl(statedata):
    print ("---------Delete proxmox_vmtpl----------------")
    print (statedata)
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
                save_proxmox_node(data)
            elif nodelabel == "ProxmoxVM":
                save_proxmox_vm(data)
            elif nodelabel == "ProxmoxVMTemplate":
                save_proxmox_vmtpl(data)

        elif event == "create_instance":
            if nodelabel == "ProxmoxNode":
                create_proxmox_node(data)
            elif nodelabel == "ProxmoxVM":
                create_proxmox_vm(data)
            elif nodelabel == "ProxmoxVMTemplate":
                create_proxmox_vmtpl(data)

        elif event == "update_instance":
            if nodelabel == "ProxmoxNode":
                update_proxmox_node(data)
            elif nodelabel == "ProxmoxVM":
                update_proxmox_vm(data)
            elif nodelabel == "ProxmoxVMTemplate":
                update_proxmox_vmtpl(data)

        elif event == "delete_instance":
            if nodelabel == "ProxmoxNode":
                delete_proxmox_node(data)
            elif nodelabel == "ProxmoxVM":
                delete_proxmox_vm(data)
            elif nodelabel == "ProxmoxVMTemplate":
                delete_proxmox_vmtpl(data)

# Asynchronous request
loop = asyncio.get_event_loop()
loop.run_until_complete(
    client.subscribe(
        query=query, 
        # handle=print
        handle=callback
    )
)
