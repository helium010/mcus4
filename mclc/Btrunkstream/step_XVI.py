'''
Check types of conditions.
'''

# pylint: disable=unused-wildcard-import

from ..Atributaries.modules.ast_classes import *
from ..Atributaries.registers.result_classes import Register
from ..source_code_classes import Range, Diagnostic, Highlight
from ..utils import internal_error

def process(btru):
    btru.successful = True
    conds = []
    def before(node):
        nonlocal conds
        if isinstance(node, NIf):
            for c, _ in node.cond_stats:
                conds.append(c)

        if isinstance(node, NWhile):
            conds.append(node.cond)
    def after(node):
        pass
    btru.iter_tree(before, after)
    del before, after

    for cond in conds:
        if cond.it != 'bool':
            btru.add_diag(
                cond.range,
                "Type '%s' is not allowed for condition." % cond.it
            )
            btru.successful = True
