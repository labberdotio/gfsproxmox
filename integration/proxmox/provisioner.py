# from proxmoxer import ProxmoxAPI

# def provision():
#     # return "Hello World--!!"
#     # TokenID = bots@pam!botstoken
#     # Secret: 2b29934d-d95e-48e4-9050-f3df9a083c5b
#     # proxmox = ProxmoxAPI('192.168.0.180', user='bots@pam', 
#     #     token_name='botstoken', token_value='2b29934d-d95e-48e4-9050-f3df9a083c5b', verify_ssl=False)
#     # proxmox = ProxmoxAPI('192.168.0.180', user='bots@pam',
#     #     password='bots123', verify_ssl=False, service='PVE')
#     # for node in proxmox.nodes.get():
#     #     for vm in proxmox.nodes(node['node']).openvz.get():
#     #         retval = retval + "<p/>{0}. {1} => {2}" .format(vm['vmid'], vm['name'], vm['status'])
#     # return retval; 

import requests

def provision(): 
    # ignore InsecureRequestWarning: Unverified HTTPS request is being made to host ...
    requests.packages.urllib3.disable_warnings() 
    PMOXAPI_HOST = "192.168.0.180"
    PMOXAPI_PORT = 8006
    PMOXAPI_PASSWORD = "..."
    PMOXAPI = "https://" + PMOXAPI_HOST + ":" + str(PMOXAPI_PORT)
    # r1 = requests.get(PMOXAPI + "/api2/json/access/ticket")
    r1 = requests.post(PMOXAPI + "/api2/json/access/ticket", data = {
        "username": "root@pam", 
        "password": PMOXAPI_PASSWORD
    }, verify=False)
    auth = r1.json()
    # print( auth.get("data", {}) )
    PVEAuthCookie = auth.get("data", {}).get("ticket")
    CSRFPreventionToken = auth.get("data", {}).get("CSRFPreventionToken")
    print( "PVEAuthCookie: " + PVEAuthCookie )
    print( "CSRFPreventionToken: " + CSRFPreventionToken )
    cookies = {
        "PVEAuthCookie": PVEAuthCookie
    }
    headers = {
        "CSRFPreventionToken": CSRFPreventionToken
    }
    # requests.get(PMOXAPI + "/api2/json/cluster", cookies=cookies, verify=False).json()
    # requests.get(PMOXAPI + "/api2/json/cluster/nextid", cookies=cookies, verify=False).json()
    # requests.get(PMOXAPI + "/api2/json/nodes", cookies=cookies, verify=False).json()
    # requests.get(PMOXAPI + "/api2/json/nodes/{node}", cookies=cookies, verify=False).json()
    # requests.get(PMOXAPI + "/api2/json/nodes/pve", cookies=cookies, verify=False).json()
    # requests.get(PMOXAPI + "/api2/json/nodes/pve/qemu", cookies=cookies, verify=False).json()
    # requests.get(PMOXAPI + "/api2/json/nodes/pve/qemu", cookies=cookies, verify=False).json()
    nextid = requests.get(PMOXAPI + "/api2/json/cluster/nextid", cookies=cookies, verify=False).json().get("data", 0)
    print(" Next ID: " + str(nextid))
    r3 = requests.post(PMOXAPI + "/api2/json/nodes/pve/qemu", data = {
        "node": "pve", 
        "vmid": nextid
    }, cookies=cookies, headers=headers, verify=False)
    nextvm = r3.json()
    print( nextvm )
    print(" Next VM: " + str(nextvm.get("data", "")))

if __name__ == '__main__':
    provision()