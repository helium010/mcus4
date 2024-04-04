'''
Infer types and values of immediate operands.
'''

# pylint: disable=unused-wildcard-import

from ..Atributaries.modules.ast_classes import *
from ..Atributaries.registers.result_classes import Register
from ..source_code_classes import Range, Diagnostic, Highlight
from ..utils import internal_error


def process(btru):
    btru.successful = True

    def before(node):
        if isinstance(node, NIMMBytes):
            node.it = 'bytes'
            bts = bytes([int(bt.text[:-2], base=0) for bt in node.bts])
            node.iv = bts

        if isinstance(node, NToken):
            if node.type in ['IMM_UINT',
                             'IMM_HEX',
                             'IMM_BIN', ]:
                node.it = 'uint'
                node.iv = int(node.text, base=0)
            elif node.type == 'IMM_STRING':
                node.it = 'string'
                node.iv = node.text[1:-1]
            elif node.type == 'IMM_BYTE':
                node.it = 'byte'
                node.iv = int(node.text[:-2],base=0)
            elif node.type == 'IMM_INT':
                node.it = 'int'
                node.iv = int(node.text[:-1])
            elif node.type == 'IMM_BYTES':
                node.it = 'bytes'
                # zbl : zero bytes length
                zbl = int(node.text[:-5], base=0)
                node.iv = bytes(zbl)
            elif node.type == 'IMM_UINTS':
                node.it = 'uints'
                # uint length
                ul = int(node.text[:-5], base=0)
                node.ul = ul
            elif node.type == 'IMM_MEMORY':
                node.it = 'bytes'
                sas, zbls = node.text.split('memory', 1)
                sa = int(sas, base=0)
                zbl = int(zbls, base=0)
                node.addr = sa
                node.iv = bytes(zbl)
            elif node.type == 'IMM_BOOL':
                node.it = 'bool'
                node.iv = True if node.text == 'true' else False

            elif node.type.startswith('IMM_'):
                internal_error()
    def after(node):
        pass
    btru.iter_tree(before, after)
    del before, after
