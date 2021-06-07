# 
# thrapp.py - Simple python thread launcher that moves jobs from scheduled 
# to completed via running state. Each scheduled job is handled by a separate
# UUID identifiable thread.
# 
import logging
import threading
from threading import Lock
import time
import uuid
# 
# Enable DEBUG here for detailed logging
# 
# logging.basicConfig(level=logging.WARNING)
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
threads_lock = Lock()
threads = []
state_lock = Lock()
state = {
    "scheduled": [
        {
            "name": "A",
            "data": "A"
        },
        {
            "name": "B",
            "data": "B"
        },
        {
            "name": "C",
            "data": "C"
        }
    ],
    "launching": [],
    "running": [],
    "completed": []
}
#
# This adds a thread to the current threads struc
#
def add_thread(UUID, new_thread):
    with threads_lock:
        threads.append({
            "uuid": UUID,
            "id": new_thread.ident,
            "thread": new_thread
        })
# 
# This adds a thread, starts it and joins to wait
# 
def run_thread(UUID, new_thread):
    add_thread(UUID, new_thread)
    new_thread.start()
    # new_thread.join()
def threadfn(UUID, job):
    logging.info(
        "Thread UUID: %s, ID: %s: starting", 
        str(UUID), 
        str(threading.current_thread().ident)
    )
    runningjob = job
    runningjob["uuid"] = UUID
    runningjob["running"] = True
    with state_lock:
        state["running"].append(runningjob)
        state["launching"].remove(job)
    time.sleep(4)
    with state_lock:
        state["running"].remove(runningjob)
        runningjob["running"] = False
        state["completed"].append(runningjob)
    logging.info(
        "Thread UUID: %s, ID: %s: finishing", 
        str(UUID), 
        str(threading.current_thread().ident)
    )
def launch_thread(job):
    global threads
    UUID = uuid.uuid1()
    launchingjob = job
    launchingjob["uuid"] = UUID
    launchingjob["running"] = False
    with state_lock:
        state["launching"].append(launchingjob)
    # new_thread = socketio.start_background_task(
    new_thread = threading.Thread(target=threadfn, args=(UUID,launchingjob,))
    # logging.info(
    #     "Main    : before running thread UUID: %s, ID: %s", 
    #     str(UUID), 
    #     str(new_thread.ident)
    # )
    # add_thread(UUID, new_thread)
    run_thread(UUID, new_thread)
    return new_thread
iteration = 0
keeprunning = True
while(keeprunning):
    # Default sleep
    sleep = 1
    iteration += 1    
    # print(state)
    logging.info("Main    :")
    logging.info("Main    :")
    logging.info("Main    :")
    logging.info("Main    : iteration %d, keep running: %s ", iteration, str(keeprunning))
    print(state)
    logging.info("Main    :")
    logging.info("Main    :")
    if state["running"]:
        keeprunning = True
        for running in state["running"]:
            logging.info("Main    : found running job: %s", str(running["name"]))
    else:
        logging.info("Main    : found no running jobs")
    if state["launching"]:
        keeprunning = True
        for running in state["launching"]:
            logging.info("Main    : found launching job: %s", str(logging["name"]))
    else:
        logging.info("Main    : found no launching jobs")
    if state["scheduled"]:
        keeprunning = True
        for schedued in state["scheduled"]:
            logging.info("Main    : found scheduled job: %s", str(schedued["name"]))
        # No sleep while scheduled jobs are present
        sleep = 0
        job = None
        with state_lock:
            job = state["scheduled"].pop()
        if job:
            new_thread = launch_thread(job)
            # new_thread.join()
    else:
        logging.info("Main    : found no scheduled jobs")
    if not state["running"] and not state["launching"] and not state["scheduled"]:
        logging.info("Main    : found no active jobs at all, exiting")
        keeprunning = False
    # else:
    #     logging.info("Main    : no more running jobs")
    #     break
    if sleep > 0:
        logging.info("Main    : All seems calm, sleeping %d seconds", sleep)
        time.sleep(sleep)
    else:
        logging.info("Main    : Scheduled jobs abound, no sleep for the wicked!")
    # if not keeprunning:
    #     break
logging.info("Main    : all done")
print(state)