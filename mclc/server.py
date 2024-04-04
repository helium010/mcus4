from flask import Flask, request
import pathlib, threading, queue, json
from threading import Condition, Lock, Event

from .utils import assert_type, error, dot_ref_from_path, path_from_dot_ref
from .manager import build_project_once
from . import context

app = Flask('server')

building_requests = []

request_queue_lock = Lock()
AtBtCd_lock = Lock()


class BuildingThread(threading.Thread):
    def run(self):
        while True:

            # wait until there is one or more requests
            while True:
                request_queue_lock.acquire()
                if len(building_requests) > 0:
                    break
                request_queue_lock.release()

            # get all request in building_requests
            events = []
            events.extend(building_requests)

            # clear building_requests
            building_requests.clear()

            # release lock
            request_queue_lock.release()
  
            # rebuild project
            AtBtCd_lock.acquire()
            build_project_once()
            AtBtCd_lock.release() 

            for bc, ppc in events:
                bc.set()
                ppc.wait()


def get_fdr():

    if 'path' not in request.args:
        return None

    # check if file exists and if file didn't change
    path_to_file = pathlib.Path(request.args['path'])
    if not path_to_file.exists(): return None

    from .utils import is_valid_p
    if not is_valid_p(path_to_file):
        return None

    return dot_ref_from_path(path_to_file)


@app.route('/hls')
def hls():

    fdr = get_fdr()
    if not fdr:
        return 'Not a valid request', 400

    # add new requet
    build_complete = Event()
    post_process_complete = Event()

    request_queue_lock.acquire()
    building_requests.append((
        build_complete,
        post_process_complete
    ))
    request_queue_lock.release()

    # wait until request have been processed
    build_complete.wait()

    # extract hls of file
    hls = []
    from . import context
    for hlt in context.btru.hls:
        if hlt.range.file_dot_ref == fdr:
            hls.append(hlt)

    # notify building thread that the result has been processed
    post_process_complete.set()

    res = {
        'hls': [hlt.dict() for hlt in hls]
    }

    return json.dumps(res)


@app.route('/diags')
def diags():

    # add new requet
    req_event = Event()
    callback_event = Event()

    request_queue_lock.acquire()
    building_requests.append((
        req_event,
        callback_event
    ))
    request_queue_lock.release()

    # wait until request have been processed
    req_event.wait()

    # extract hls of file
    diags = {}

    from . import context
    for dg in context.btru.diags:
        # fps : file path str
        fps = path_from_dot_ref(dg.range.file_dot_ref).as_posix()
        if fps not in diags:
            diags[fps] = []
        diags[fps].append(dg)

    res_diags = []
    for fps, dgs in diags.items():
        res_diags.append((
            fps,
            [dg.dict() for dg in dgs]
        ))

    # notify building thread that the result has been processed
    callback_event.set()

    res = {
        'diags': res_diags
    }

    return json.dumps(res)


@app.route('/gtd')  # gtd : go to definition
def hover():
    fdr = get_fdr()
    if not fdr: return 'Not a valid request', 400
    if not all([par in request.args for par in ['ln', 'col']]): return 'Not a valid request', 400

    ln = int(request.args['ln'])
    col = int(request.args['col'])

    from .Eiyuu.lancer import definition_object_range_from_position
    AtBtCd_lock.acquire()
    mdr = definition_object_range_from_position(fdr, ln, col)
    AtBtCd_lock.release()

    if mdr is None:
        res = {'ok' : False}
    else:
        res = {'ok' : True}
        res['fps'] = path_from_dot_ref(mdr.file_dot_ref).as_posix()
        res['range'] = mdr.dict()
    return json.dumps(res)
    

    

def start_server():

    build_project_once()

    building_thread = BuildingThread()
    building_thread.start()

    app.run(host='0.0.0.0', port=23333)
