'''
Infer types of local var def.
'''

# pylint: disable=unused-wildcard-import

from ..Atributaries.modules.ast_classes import *
from ..Atributaries.registers.result_classes import Register
from ..source_code_classes import Range, Diagnostic, Highlight
from ..utils import internal_error


def process(btru):
    btru.successful = True

    def before(node):
        if isinstance(node, NLclVarDef):
            node.it = node.id.st

    def after(node):
        pass
    btru.iter_tree(before, after)
    del before, after
