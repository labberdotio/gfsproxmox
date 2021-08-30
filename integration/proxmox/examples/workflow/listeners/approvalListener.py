
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
            chain: ["approvalOf"]
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

        # if approval.get("status") == "assign":
        # if event.get("event") == "update_node" and \
        #     approval.get("status") == "approve":
        if approval.get("status") == "approve":
            amount = float(invoice.get("amount"))
            if amount <= 10.0:
                print( " Invoice amount " + str(amount) + " is less than or equal to 10.0, updating approval with status approved" )
                clicall("exec query @" + cwd + "/queries/approveApproval.query --data id=\"%s\"" % (
                    approvalid
                ))

            # elif amount > 100.0:
            #     print( " Invoice amount " + str(amount) + " is more than 100.0, updating approval with status unapproved" )
            #     clicall("exec query @" + cwd + "/queries/unapproveApproval.query --data id=\"%s\"" % (
            #         approvalid
            #     ))
            # else:
            elif not approval.get("reviewOf"):

                print( " Invoice amount " + str(amount) + " is more than 10.0, approval requires a review " )
                review = clicall("exec query @" + cwd + "/queries/createReview.query --data status=\"%s\" notice=\"%s\" reviewer=\"%s\"" % (
                    "review", 
                    "Begin review process", 
                    "Some Name"
                ))

                print( " Updating approval with new review, awaiting review status" )
                reviewid = review.get("data", {}).get("createReview", {}).get("instance", {}).get("id")
                if approvalid and reviewid:
                    clicall("link reviewOf --from \"%s\" --to \"%s\"" % (
                        reviewid, 
                        approvalid
                    ))

                print( " Updating approval with status review" )
                clicall("exec query @" + cwd + "/queries/reviewApproval.query --data id=\"%s\"" % (
                    approvalid
                ))

        elif event.get("event") == "update_node" and \
            approval.get("status") == "review" and \
            approval.get("reviewOf"):

            review = approval.get("reviewOf")[0]
            reviewid = review.get("id")

            if review.get("status") == "approved":
                print( " Invoice review is updated to approved, approving approval" )
                clicall("exec query @" + cwd + "/queries/approveApproval.query --data id=\"%s\"" % (
                    approvalid
                ))

            elif review.get("status") == "unapproved":
                print( " Invoice review is updated to unapproved, unnapriving approval" )
                clicall("exec query @" + cwd + "/queries/unapproveApproval.query --data id=\"%s\"" % (
                    approvalid
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
