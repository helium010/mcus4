'''
Check values of immediate operands.
'''


# pylint: disable=unused-wildcard-import, function-redefined

from ..Atributaries.modules.ast_classes import *
from ..source_code_classes import Range, Diagnostic, Highlight
from . import ProcessError



def process(btru):
    btru.successful = True
    def before(node):
        if isinstance(node, NToken):
            if node.type == 'IMM_BYTE':
                iv = int(node.text[:-2], base=0)
                if iv > 255:
                    btru.add_diag(
                        node.range,
                        "'%d' is not a valid byte value (0 <= v < 256)." % iv
                    )
                    btru.successful = False
    def after(node):
        pass
    btru.iter_tree(before, after)
    del before, after