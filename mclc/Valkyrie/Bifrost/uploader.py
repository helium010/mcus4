from pathlib import Path
from . import open_session
from pyocd.flash.file_programmer import FileProgrammer
from ...utils import internal_error




def upload():
    ep = Path('./build/program.elf')
    if not ep.exists(): internal_error()

    session = open_session()

    fp = FileProgrammer(session)
    fp.program(ep.absolute().__str__(), file_format='elf')
    
    session.close()

    