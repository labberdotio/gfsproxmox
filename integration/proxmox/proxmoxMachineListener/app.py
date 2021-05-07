
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

# from proxmoxer import ProxmoxAPI
from implementation import create_handler
from implementation import update_handler
from implementation import delete_handler
from implementation import link_handler


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

GFSHOST = "localhost" # "192.168.0.160"
GFSPORT = 5000
TYPE="ProxmoxMachine"

LISTENERADDR = "0.0.0.0"
LISTENERPORT = 5002

state = {
    "GFSHOST": GFSHOST, 
    "GFSPORT": GFSPORT, 
    "endpoint": "ws://" + GFSHOST + ":" + str(GFSPORT) + "/gfs1/graphql/subscriptions", 
    "active": False, 
     "type": TYPE, 
    "query": """subscription """ + TYPE + """Subscriber {
  """ + TYPE + """ {
    event, 
    id, 
    label, 
    sourceid, 
    sourcelabel, 
    targetid, 
    targetlabel, 
    chain, 
    node {
       id,
       name
    }
  }
}
""", 
    "models": []
}

client = GraphqlClient(
    endpoint=state.get("endpoint")
)

def callback(data = {}):

    typedata = data.get("data", {}).get(TYPE, {})
    typenode = typedata.get("node", {})

    print(" ")
    print(" New " + TYPE + " event: ")
    print(" Event: " + str( typedata.get("event", "")) )
    print(" Id: " + str( typedata.get("id", "")) )
    print(" Label: " + str( typedata.get("label", "")) )
    print(" SourceId: " + str( typedata.get("sourceid", "")) )
    print(" SourceLabel: " + str( typedata.get("sourceid", "")) )
    print(" TargetId: " + str( typedata.get("targetid", "")) )
    print(" TargetLabel: " + str( typedata.get("targetlabel", "")) )
    print(" Chain: " + str( typedata.get("chain", "")) )
    # print(data)
    # print(typedata)
    print(" ")

    event = typedata.get("event", None)
    id = typedata.get("id", None)
    label = typedata.get("label", None)
    sourceid = typedata.get("sourceid", None)
    sourcelabel = typedata.get("sourcelabel", None)
    targetid = typedata.get("targetid", None)
    targetlabel = typedata.get("targetlabel", None)
    chain = ", ".join(typedata.get("chain", []))

    typenodeid = typenode.get("id")
<<<<<<< HEAD:integration/proxmox/app.py

    typenodedesc = TYPE + ": " + typenode.get("name") + " - " + typenode.get("bootdisk") + " bootdisk, " + typenode.get("cores") + " cores, " + typenode.get("memory") + " MB RAM, " + typenode.get("numa") + " NUMA setting, "  + typenode.get("ostype") + " ostype, " + typenode.get("sockets") + " sockets. "
=======
    typenodedesc = TYPE + "(" + typenodeid + ")"
    for key in typenode:
        typenodedesc += ", " + key + ": " + typenode.get(key, "[NONE]")
>>>>>>> 109331d (Broke out and cleaned up event listeners):integration/proxmox/proxmoxMachineListener/app.py

    statedata = {
        "event": event, 
        "id": id, 
        "label": label, 
        "sourceid": sourceid, 
        "sourcelabel": sourcelabel, 
        "targetid": targetid, 
        "targetlabel": targetlabel, 
        "chain": chain,
        "data": typenode,
        "description": typenodedesc
    }

    # print(statedata)
    # print(" ")

    state.get("models", []).insert(0, statedata)

    # socketio.emit(
    #     'update', {
    #         'data': statedata
    #     }
    # )

    socketio.emit(
        'update', statedata
    )

    # delegate to implementation.py methods
    if event == "create_node":
        create_handler(statedata)
    elif event == "update_node":
        update_handler(statedata)
    elif event == "delete_node":
        delete_handler(statedata)
    elif event == "create_link":
        link_handler(statedata)

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
        type = state.get("type", TYPE), 
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
    client = GraphqlClient(
        endpoint=state.get("endpoint")
    )
    socketio.run(app, host=LISTENERADDR, port=LISTENERPORT)
