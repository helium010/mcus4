import usb, time

defined_commands = {}


def command(fun):
    cmd = fun.__name__.replace('_', '-')
    defined_commands[cmd] = fun

    return fun


# pragma command definitions
@command
def __help():
    print('commands:')
    keys = list(defined_commands)
    keys.sort()
    for cmd in keys:
        print(' ' * 4 + cmd)


@command
def serve():
    from . import server
    server.start_server()


@command
def test():
    from . import get_test_data
    values = get_test_data()
    print(values)

import sys
if len(sys.argv) == 1:
    __help()
else:
    cmd = sys.argv[1]
    if cmd not in defined_commands:
        exit(1)
    cmd_fun = defined_commands[cmd]
    cmd_fun()
