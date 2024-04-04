# pylint: disable=unused-wildcard-import
import importlib, pathlib

from ...Atributaries.modules.ast_classes import *
from ...Atributaries.registers.result_classes import Register
from ...source_code_classes import Range, Diagnostic, Highlight
from ...utils import internal_error, assert_type
from . import GenContext, assembly_line
 





al_dir = pathlib.Path(__file__).parent.joinpath('assembly_line')

step_py_mod_names = []
for stf in al_dir.glob('step_*.py'):
    step_py_mod_names.append(stf.name[:-3])


step_py_mod_names.sort()

step_py_mods = []

for mn in step_py_mod_names:
    step_py_mods.append(
        importlib.import_module('.assembly_line.' + mn, __package__)
    )



 
def gen_c(btru):
    gc = GenContext(btru)

    for pm in step_py_mods:
        pm.process(gc)

