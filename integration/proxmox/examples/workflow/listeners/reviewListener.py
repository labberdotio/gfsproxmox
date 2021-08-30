
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
        Invoice(
            events: ["create_link", "update_node"], 
            chain: ["approvalOf", "reviewOf"]
        ) {
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

    print( " >> EVENT: " + event.get('event') + ", CHAIN: " + str(event.get('chain')))
    print( event.get("node", {}) )

    if invoice.get("approvalOf"):

        approval = invoice.get("approvalOf")[0]
        approvalid = approval.get("id")

        if approval.get("reviewOf"):

            review = approval.get("reviewOf")[0]
            reviewid = review.get("id")

            # if approval.get("status") == "assign":
            # if event.get("event") == "update_node" and \
            #     review.get("status") == "review":
            if review.get("status") == "review":
                amount = float(invoice.get("amount"))
                if amount <= 100.0:
                    print( " Invoice amount " + str(amount) + " is less than or equal to 100.0, updating review with status approved" )
                    clicall("exec query @" + cwd + "/queries/approveReview.query --data id=\"%s\"" % (
                        reviewid
                    ))

                elif amount > 100.0:
                    print( " Invoice amount " + str(amount) + " is is more than 100.0, updating review with status unapproved" )
                    clicall("exec query @" + cwd + "/queries/unapproveReview.query --data id=\"%s\"" % (
                        reviewid
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
