
from threading import Lock

from flask import Flask
from flask import render_template
from flask import request
from flask import Response

from flask_socketio import SocketIO
from flask_socketio import emit
from flask_socketio import disconnect

from proxmoxer import ProxmoxAPI

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

def background_thread():
    """Example of how to send server generated events to clients."""
    while True:
        socketio.sleep(10)
        socketio.emit(
            'response', {
                'data': 'Ping!'
            }
        )

# @app.route('/')
# def hello():
#     # return "Hello World--!!"
#     # TokenID = bots@pam!botstoken
#     # Secret: 2b29934d-d95e-48e4-9050-f3df9a083c5b
#     proxmox = ProxmoxAPI('192.168.0.180', user='bots', token_name='bots@pam', token_value='2b29934d-d95e-48e4-9050-f3df9a083c5b', verify_ssl=False)
#     for node in proxmox.nodes.get():
#         for vm in proxmox.nodes(node['node']).openvz.get():
#             retval = retval + "<p/>{0}. {1} => {2}" .format(vm['vmid'], vm['name'], vm['status'])
#     return retval; 

@app.route('/')
def index():
    return render_template(
        'index.html', 
        async_mode=socketio.async_mode
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
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit(
        'response', {
            'data': 'Connect'
        }
    )

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    # app.run(host= '0.0.0.0')
    socketio.run(app)
