import json, pathlib, math, threading, usb, time


def connect_to_servant():
    dev = usb.core.find(idVendor=0x455a, idProduct=0x455a)
    cfg = dev.get_active_configuration()
    dev.set_configuration(cfg)
    intf = cfg[(0, 0)]
    ep_in = None
    ep_out = None
    dev.reset()
    for ep in intf.endpoints():
        if ep.bEndpointAddress == 1:
            ep_out = ep
        if ep.bEndpointAddress == 0x81:
            ep_in = ep

    if any([ep is None for ep in (ep_out, ep_in)]):
        print('error')
        exit(1)

    return ep_out, ep_in, dev


def get_test_data():

    # pylint: disable=unused-variable

    ep_out, ep_in, dev = connect_to_servant()
    ep_in: usb.core.Endpoint
    ep_out: usb.core.Endpoint

    

    cmds = [
        1,
        2,
        3,
        4,
        5
    ]


    for cmd in cmds:

        ep_out.write(bytes([1, cmd]))
        res = b''
        while True:
            _res = ep_in.read(2000)
            if len(_res) == 0:
                break

            res += _res
        
        values = []
        tmp = 0
        for i, b in enumerate(res):
            if i % 2 == 0:
                tmp = int(b)
            else:
                tmp = tmp + int(b) * 256
                values.append(tmp)

        time.sleep(0.1)

    usb.util.dispose_resources(dev)
    
    return {
        'x' : [i / 10 for i in range(len(values))],
        'y': [v * 3.3 / (1 << 12) for v in values]
    }