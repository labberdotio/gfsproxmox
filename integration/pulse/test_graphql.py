import requests
import polling2
import json
import threading
import time
from requests_toolbelt.utils import dump
from python_graphql_client import GraphqlClient

GFSAPI_HOST = "192.168.0.160" # "192.168.0.160"
GFSAPI_PORT = 5000

GFSAPI = "http://" + GFSAPI_HOST + ":" + str(GFSAPI_PORT)

GFSAPI_ALL_NODES_URL = GFSAPI + "/api/v1.0/gfs1/graph"
GFSAPI_ALL_INSTANCES_OF_TYPE = GFSAPI + "/api/v1.0/gfs1/vertex?label={type}"

GFSAPI_GRAPH_URL = GFSAPI + "/gfs1/graphql"
gfs_gqlclient = GraphqlClient(endpoint=GFSAPI_GRAPH_URL)

def current_milli_time():
    return round(time.time())

update_ip = """
mutation updateIp
   (
       $id:String!, 
       $name:String, 
       $address:String, 
    ) 
{                
    updateIp(id:$id, name:$name, address:$address, ) {                    
        instance {                        
            id, name, address,                      
        },                    
        ok                
    } 
}
"""
ip_vars = """
{
  "id": "82", 
  "name": "test",
  "address": "test"
}
"""

def main():
    data = gfs_gqlclient.execute(
        query=update_ip, 
        variables=ip_vars
    )
    print (data)

if __name__ == "__main__":
    main()
    # print (current_milli_time())