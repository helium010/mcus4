from .Atributaries import manager as Amngr
from .Btrunkstream import manager as Bmngr
from .Valkyrie.generate_c import manager as GCMngr
from .Valkyrie.Bifrost import open_session, uploader
from . import context
from .utils import print_error

def build_project_once():
    atri = Amngr.process()

    btru = Bmngr.process(atri)
    context.btru = btru
    return btru
    


def build_elf():
    btru = build_project_once()
    if not btru.successful:
        print_error("Building Failed.")
        exit(1)
    GCMngr.gen_c(btru)

    