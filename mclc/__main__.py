from pathlib import Path
from .utils import print_error, print_ok

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
def init():
    proj_dir = Path('.').joinpath('mcl-src')
    if proj_dir.exists():
        print_error("directory 'project' already exists")
        exit(1)
    proj_dir.mkdir()
    proj_dir.joinpath('regs').mkdir()
    mod_dir = proj_dir.joinpath('mods')
    mod_dir.mkdir()
    proj_dir.joinpath('system-init').touch()
    proj_dir.joinpath('system-mainloop').touch()

    print_ok("Initialized new project.")

@command
def serve():
    from .server import start_server
    start_server()

@command
def build_elf():
    from .manager import build_elf
    build_elf()

@command 
def debug(): 
    from .manager import build_elf
    build_elf()
    from .Valkyrie.Bifrost import debugger

    debugger.start_server()










import sys
if len(sys.argv) == 1:
    __help()
else:
    cmd = sys.argv[1]
    if cmd not in defined_commands:
        print_error("command %s is not defined" % cmd)
    cmd_fun = defined_commands[cmd]
    cmd_fun()