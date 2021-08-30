
import asyncio
import subprocess

import simplejson as json

from python_graphql_client import GraphqlClient



listenerEndpoint = "ws://localhost:5000/gfs1/graphql/subscriptions"
queryEndpoint = "http://localhost:5000/gfs1/graphql"

host = "localhost"
cwd = "./"

env = {
    "GFS_HOST": host
}



listenerClient = GraphqlClient(
    endpoint=listenerEndpoint
)

queryClient = GraphqlClient(
    endpoint=queryEndpoint
)




def clicall(command):

    executable = "/bin/sh"

    calloutput = subprocess.check_output(
        [
            executable, 
            "-c", 
            "GFS_HOST=" + host + " gfscli " + command
        ],
        cwd = cwd,
        env = env
    )

    # return calloutput
    return json.loads(calloutput)



listenerQuery = """
    subscription invoiceEvent {
        Invoice {
            event, 
            chain, 
            node {
                id, 
                name, 
                description, 
                amount, 
                status, 
                approvalOf {
                    id, 
                    status, 
                    notice, 
                    approver, 
                    reviewOf {
                        id, 
                        status, 
                        notice, 
                        reviewer
                    }
                }
            }
        }
    }
"""



def listenerCallback(data = {}):

    event = data.get("data", {}).get("Invoice", {})
    invoice = event.get("node", {})
    invoiceid = invoice.get("id")

    print( " >> EVENT: " + event.get('event') + ", CHAIN: " + str(event.get('chain')))
    print( event.get("node", {}) )

    if event.get("event") == "create_node" and \
        not invoice.get("approvalOf"):

        print( " New invoice received, creating new approval assigned to group" )
        approval = clicall("exec query @" + cwd + "/queries/createApproval.query --data status=\"%s\" notice=\"%s\" approver=\"%s\"" % (
            "approve", 
            "Request for approval", 
            "Some Name"
        ))

        print( " Updating invoice with new approval, awaiting approval status" )
        approvalid = approval.get("data", {}).get("createApproval", {}).get("instance", {}).get("id")
        if invoiceid and approvalid:
            clicall("link approvalOf --from \"%s\" --to \"%s\"" % (
                approvalid, 
                invoiceid
            ))

        print( " Updating invoice with status received" )
        clicall("exec query @" + cwd + "/queries/receiveInvoice.query --data id=\"%s\"" % (
            invoiceid
        ))

    elif event.get("event") == "update_node" and \
        invoice.get("status") == "received" and \
        invoice.get("approvalOf"):

        approval = invoice.get("approvalOf")[0]
        approvalid = approval.get("id")

        if approval.get("status") == "approved":
            print( " Invoice approval is updated to approved, approving invoice" )
            clicall("exec query @" + cwd + "/queries/approveInvoice.query --data id=\"%s\"" % (
                invoiceid
            ))

        elif approval.get("status") == "unapproved":
            print( " Invoice approval is updated to unapproved, unapproving invoice" )
            clicall("exec query @" + cwd + "/queries/unapproveInvoice.query --data id=\"%s\"" % (
                invoiceid
            ))

    print( "" )
    print( "" )



# Asynchronous request
loop = asyncio.get_event_loop()
loop.run_until_complete(
    listenerClient.subscribe(
        query=listenerQuery, 
        handle=listenerCallback
        # callback=callback
    )
)
