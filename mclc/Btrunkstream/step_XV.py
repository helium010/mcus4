'''
Check types of initial values in variable definition.
'''

# pylint: disable=unused-wildcard-import

from ..Atributaries.modules.ast_classes import *
from ..Atributaries.registers.result_classes import Register
from ..source_code_classes import Range, Diagnostic, Highlight
from ..utils import internal_error

def process(btru):
    btru.successful = True
    def before(node):
        if isinstance(node, NVarDef):
            if node.init_value.it == 'bytes' and node.type.st == 'uints':
                return
            if node.init_value.it != node.type.st:
                btru.add_diag(
                    node.init_value.range,
                    "Initial value's type '%s' is incompatible with variable's type '%s'." % (
                        node.init_value.it,
                        node.type.st
                    )
                )
                btru.successful = False

    def after(node):
        pass
    btru.iter_tree(before, after)
    del before, after