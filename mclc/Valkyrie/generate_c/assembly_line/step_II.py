'''
Generate variable declaration.
'''

# pylint: disable=unused-wildcard-import
import random, string, datetime

from ....Atributaries.modules.ast_classes import *
from .pgfs import sym_decl


def process(gc):
    btru = gc.btru

    def before(node):
        if isinstance(node, NVarDef):
            gc.sb.append_lines(sym_decl.gen(gc, node))

    def after(node):
        pass
    btru.iter_tree(before, after)
    del before, after
