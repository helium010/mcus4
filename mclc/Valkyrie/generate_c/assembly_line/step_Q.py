'''
Generate function definitions.
'''

# pylint: disable=unused-wildcard-import
import random, string, datetime

from ....Atributaries.modules.ast_classes import *
from .pgfs import fun_def


def process(gc):
    btru = gc.btru

    def before(node):
        if isinstance(node, NFunDef):
            gc.sb.append_lines(fun_def.gen(gc, node))

    def after(node):
        pass
    btru.iter_tree(before, after)
    del before, after

