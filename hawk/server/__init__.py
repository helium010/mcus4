import json, pathlib, math, threading, usb, time
from flask import Flask
from .. import connect_to_servant


app = Flask('hawk')


@app.route('/')
def index():
    idx = pathlib.Path(__file__).parent.joinpath('html', 'index.html').read_text()
    return idx


from .. import get_test_data

@app.route('/data')
def data():
    values = get_test_data()

    return json.dumps(values)

    


def start_server():

    app.run(host='0.0.0.0', port=23335)
