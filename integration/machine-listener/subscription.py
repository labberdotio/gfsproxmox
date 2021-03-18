
import asyncio

from python_graphql_client import GraphqlClient

GFSHOST = "localhost"
GFSPORT = 5000

endpoint = "ws://" + GFSHOST + ":" + str(GFSPORT) + "/gfs1/graphql/subscriptions"

client = GraphqlClient(
    endpoint=endpoint
)

"""
 New Machine event: 
 Event: create_node
 Chain: []
{
	'event': 'create_node',
	'chain': [],
	'node': {
		'id': '68',
		'name': 'botnode11',
		'arch': 'x86_64',
		'cpus': '1',
		'cores': '2',
		'memory': '4096',
		'ht': 'ht',
		'Configured': [{
			'id': '69',
			'name': 'net6E:C6:6C:28:6F:EE',
			'hwaddr': '6E:C6:6C:28:6F:EE',
			'AssignedTo': [{
				'id': '70',
				'name': 'devIp10.88.88.202',
				'address': '10.88.88.202'
			}]
		}]
	}
}
"""

query = """
subscription MachineSubscriber {
  Machine {
    event, 
    chain, 
    node {
      id, 
      name, 
      arch, 
      cpus, 
      cores, 
      memory, 
      ht, 
      Configured {
        id, 
        name, 
        hwaddr, 
        AssignedTo {
          id, 
          name, 
          address
        }
      }
    }
  }
}
"""

def callback(data = {}):
    print(" ")
    print(" New Machine event: ")
    print(" Event: " + str( data.get("data", {}).get("Machine", {}).get("event", "")) )
    print(" Chain: " + str( data.get("data", {}).get("Machine", {}).get("chain", "")) )
    # print(data)
    print(data.get("data", {}).get("Machine", {}))
    print(" ")

# Asynchronous request
loop = asyncio.get_event_loop()
loop.run_until_complete(
    client.subscribe(
        query=query, 
        handle=callback
        # handle=print
    )
)
