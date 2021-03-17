from flask import Flask
from proxmoxer import ProxmoxAPI

app = Flask(__name__)

@app.route('/')
def hello():
    # return "Hello World--!!"
    # TokenID = bots@pam!botstoken
    # Secret: 2b29934d-d95e-48e4-9050-f3df9a083c5b
    proxmox = ProxmoxAPI('192.168.0.180', user='bots', token_name='bots@pam', token_value='2b29934d-d95e-48e4-9050-f3df9a083c5b', verify_ssl=False)
    for node in proxmox.nodes.get():
        for vm in proxmox.nodes(node['node']).openvz.get():
            retval = retval + "<p/>{0}. {1} => {2}" .format(vm['vmid'], vm['name'], vm['status'])
    return retval; 

if __name__ == '__main__':
    app.run(host= '0.0.0.0')

