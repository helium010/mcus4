from .result_classes import Btru
import importlib, pathlib

cur_dir = pathlib.Path(__file__).parent

step_py_mod_names = []
for stf in cur_dir.glob('step_*.py'):
    step_py_mod_names.append(stf.name[:-3])


step_py_mod_names.sort()

step_py_mods = []

for mn in step_py_mod_names:
    step_py_mods.append(
        importlib.import_module('.' + mn, __package__)
    )

def process(atri):
    btru = Btru(atri)
    for pm in step_py_mods:
        if not btru.successful:
            break
        btru.successful = False
        pm.process(btru)
    return btru