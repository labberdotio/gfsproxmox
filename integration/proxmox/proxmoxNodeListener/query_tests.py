import os
import requests
import json
import time
from gfsgql import GFSGQL

GFSAPI_HOST = os.getenv('GFSAPI_HOST')
GFSAPI_PORT = os.getenv('GFSAPI_PORT')

gfs_gqlclient = GFSGQL (
    gfs_host = GFSAPI_HOST, # gfs_host,
    gfs_port = GFSAPI_PORT, # gfs_port,
    gfs_username = None, # gfs_username,
    gfs_password = None, # gfs_password,
)

def main():
    createVM = gfs_gqlclient.gqlexec("""
        mutation createProxmoxVMTemplate($vmID:String!, $name:String!, $vmName: String!, $hostedOn:String, $template:String!, $status:String) {
            create ProxmoxVMTemplate  (
                name: $name,
                vmId: $vmID,
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
            "name": vmname_composite,
            "vmID": vm_id,
            "vmName": vm_name,
            "hostedOn": proxmox_id,
            "template": "1",
            "status": "TEST"
        }
    )

if __name__ == "__main__":
    main()
