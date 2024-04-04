from pathlib import Path
import json
from flask import Flask, request
from . import open_session
from pyocd.flash.file_programmer import FileProgrammer
from ...utils import internal_error
from ...Eiyuu.lancer import fld_object_from_position


def get_fdr():

    if 'path' not in request.args:
        return None

    # check if file exists and if file didn't change
    path_to_file = Path(request.args['path'])
    if not path_to_file.exists(): return None

    from ...utils import is_valid_p, dot_ref_from_path
    if not is_valid_p(path_to_file):
        return None

    return dot_ref_from_path(path_to_file)


_session = None

def get_session():
    ep = Path('./build/program.elf')
    if not ep.exists(): internal_error()

    global _session

    if _session is not None:
        return _session

    _session = open_session()

    fp = FileProgrammer(_session)
    fp.program(ep.absolute().__str__(), file_format='elf')

    _session.target.resume()

    return _session


app = Flask('debug server')

# pylint: disable=unused-variable
@app.route('/hover')
def hover():
    fdr = get_fdr()
    if not fdr:
        return '', 400


    if not request.args['path'].endswith('.reg'):
        return '', 400

    if not set(['ln', 'col']).issubset(set(request.args.keys())):
        return '', 400

    fld = fld_object_from_position(
        fdr,
        int(request.args['ln']),
        int(request.args['col']),
    )
    if fld is None: return '', 404

    values = []
    
    addrs = fld.reg.addresses
    mds = ''
    if len(addrs) == 0: internal_error()

    session = get_session()

    avs = [] # address-value pairs

    for addr in addrs:
        # rv : register value
        rv = session.target.read32(addr)
        # fv : field value
        fv = ( rv >> fld.bits[1] ) % (1 << (fld.bits[0] + 1 - fld.bits[1]))
        avs.append((
            addr, fv
        ))



    if len(avs) == 1:
        mds += '%d' % avs[0][1]
    else:
        mds += "Addr | Value\n-|-\n"
        for addr, v in avs:
            mds += "`%#.8X` | %d\n" % (addr, v)


    res = {
        'mds': mds
    }

    return json.dumps(res), 200


@app.route('/halt')
def halt():
    session = get_session()
    session.target.halt()
    return '', 200

@app.route('/resume')
def resumt():
    session = get_session()
    session.target.resume()
    return '', 200
    






def start_server():


    get_session()
    app.run(host='0.0.0.0', port=23334)
