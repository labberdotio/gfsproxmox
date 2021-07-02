#!python
from gremlinfs.gfsgql import GFSGQL
# 
# Main
# 
if __name__ == '__main__':
    gfs_host = "localhost"
    gfs_port = "5000"
    gfs_username = None
    gfs_password = None
    gqlClient = GFSGQL(
        gfs_host = gfs_host,
        gfs_port = gfs_port,
        gfs_username = gfs_username,
        gfs_password = gfs_password,
    )
    # Node details
    pveName = "pve"
    pveId = None # to be discovered
    # VM details
    vmName = "ProxmoxVM"
    vmId = None # to be discovered
    pveNode = gqlClient.gqlexec(
        """
query pveNode($pveName:String, ) {
  ProxmoxNodes(
    name: $pveName
  ) {
    id,
    name
  }
}
        """,
        {
            "pveName": pveName,
        }
    )
    # print(pveNode)
    pveId = pveNode.get("data", {}).get("ProxmoxNodes", [])[0].get("id")
    print(" ")
    print(" PVE NODE ID: " + pveId)
    print(" ")
    createVM = gqlClient.gqlexec(
        """
mutation createVM($vmName:String!, $hostedOn:String) {
  createProxmoxVM (
    name: $vmName,
    setHostedOn: {
      id: $hostedOn
    }
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
            "vmName": vmName,
            "hostedOn": pveId
        }
    )
    # print(createVM)
    vmId = createVM.get("data", {}).get("createProxmoxVM", {}).get("instance", {}).get("id")
    print(" ")
    print(" CREATE VM ID: " + vmId)
    print(" ")
    getVM = gqlClient.gqlexec(
        """
query getVM($vmId:String!, ) {
  ProxmoxVM(
    id: $vmId
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
            "vmId": vmId
        }
    )
    # print(getVM)
    # print(vmId)
    print(" ")
    print(" VERIFY VM ID: " + vmId)
    print(" VERIFY VM DEPLOYED ON: " + getVM.get("data", {}).get("ProxmoxVM", {}).get("HostedOn", {}).get("id"))
    print(" VERIFY VM DEPLOYED ON: " + getVM.get("data", {}).get("ProxmoxVM", {}).get("HostedOn", {}).get("name"))
    print(" ")