
import asyncio
# import threading

from threading import Lock

from flask import Flask
from flask import render_template
from flask import request
from flask import Response

from flask_socketio import SocketIO
from flask_socketio import emit
from flask_socketio import disconnect

from python_graphql_client import GraphqlClient

from proxmoxer import ProxmoxAPI



# 
# 
# 

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

thread = None
thread_lock = Lock()

# 
# 
# 

GFSHOST = "localhost"
GFSPORT = 5000

state = {
    "GFSHOST": GFSHOST, 
    "GFSPORT": GFSPORT, 
    "endpoint": "ws://" + GFSHOST + ":" + str(GFSPORT) + "/gfs1/graphql/subscriptions", 
    "active": False, 
    "query": """
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
      ht
    }
  }
}
""", 
    "models": []
}

# 
# 
# 

client = GraphqlClient(
    endpoint=state.get("endpoint")
)

# 
# 
# 

def callback(data = {}):

    machine = data.get("data", {}).get("Machine", {})
    machinenode = machine.get("node", {})

    print(" ")
    print(" New Machine event: ")
    print(" Event: " + str( machine.get("event", "")) )
    print(" Chain: " + str( machine.get("chain", "")) )
    # print(data)
    print(machine)
    print(" ")

    event = machine.get("event")
    chain = ", ".join(machine.get("chain", []))

    machinenodeid = machinenode.get("id")
    machinenodedesc = "Machine: " + machinenode.get("name") + " (" + machinenode.get("arch") + ") " + machinenode.get("cpus") + " cpus, " + machinenode.get("cores") + " cores, " + machinenode.get("memory") + " Mb."

    statedata = {
        "event": event, 
        "chain": chain, 
        "id": machinenodeid, 
        "description": machinenodedesc
    }

    print(statedata)
    print(" ")

    # state.get("models", []).append(machine)
    state.get("models", []).append(statedata)

    # socketio.emit(
    #     'update', {
    #         'data': statedata
    #     }
    # )

    socketio.emit(
        'update', statedata
    )

def background_thread():
    """Example of how to send server generated events to clients."""

    state["active"] = True

    # Asynchronous request
    # loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        client.subscribe(
            query=state.get("query"), 
            handle=callback
            # handle=print
        )
    )

    state["active"] = False

def launch_background_thread():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

launch_background_thread()

# 
# 
# 

@app.route('/')
def index():
    status = "danger"
    if state.get("active", False):
        status = "success"
    return render_template(
        'index.html', 
        # state = state, 
        GFSHOST = state.get("GFSHOST"), 
        GFSPORT = state.get("GFSPORT"), 
        active = state.get("active", False), 
        status = status, 
        models = state.get("models", []), 
        async_mode = socketio.async_mode
    )

@socketio.event
def fromclient(message):
    emit('response', {
        'data': 'Received from client: ' + message['data']
    }
)

@socketio.event
def disconnect_request():

    def can_disconnect():
        disconnect()

    # for this emit we use a callback function
    # when the callback function is invoked we know that the message has been
    # received and it is safe to disconnect
    emit(
        'response', {
            'data': 'Disconnect!'
        },
        callback=can_disconnect
    )

@socketio.event
def connect():
    # 
    emit(
        'response', {
            'data': 'Connect'
        }
    )

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

# 
# 
# 

if __name__ == '__main__':
    # app.run(host= '0.0.0.0')
    socketio.run(app, host='0.0.0.0', port=5001)
