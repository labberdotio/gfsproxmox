
# import asyncio
import subprocess

import simplejson as json

def clicall(command):

    host = "localhost"

    executable = "/bin/sh"
    cwd = "./"
    env = {
        "GFS_HOST": host
    } 

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

if __name__ == '__main__':

    # host = "localhost"

    # executable = "/bin/sh"
    # cwd = "./"
    # env = {
    #     "GFS_HOST": host
    # }

    # calloutput = subprocess.check_output(
    #     [
    #         executable, 
    #         "-c", 
    #         "GFS_HOST=" + host + " gfscli exec query @" + cwd + "/listInvoices.query --data name=invoice1"
    #     ],
    #     cwd = cwd,
    #     env = env
    # )
    # print(calloutput)
    calloutput = clicall("exec query @" + cwd + "/listInvoices.query --data name=invoice1")
    print(calloutput)

    # calloutput = subprocess.check_output(
    #     [
    #         executable, 
    #         "-c", 
    #         "GFS_HOST=" + host + " gfscli exec query @" + cwd + "/createApproval.query --data status=\"%s\" notice=\"%s\" approver=\"%s\"" % (
    #             "assign", 
    #             "Assigning approver group", 
    #             "Some Name"
    #         )
    #     ],
    #     cwd = cwd,
    #     env = env
    # )
    # print(calloutput)
    calloutput = clicall("exec query @" + cwd + "/createApproval.query --data status=\"%s\" notice=\"%s\" approver=\"%s\"" % (
        "assign", 
        "Assigning approver group", 
        "Some Name"
    ))
    print(calloutput)

    # data = queryClient.execute(
    #     query=createApprovalQuery, 
    #     variables={
    #         "status": "assign", 
    #         "notice": "Assigning approver group",
    #         "approver": "Some Name"
    #     }
    # )
    # print(data)
