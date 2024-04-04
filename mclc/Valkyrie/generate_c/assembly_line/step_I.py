'''
Generate C symbol table.
'''


# pylint: disable=unused-wildcard-import
import random, string, datetime

from ....Atributaries.modules.ast_classes import *
from ....Atributaries.registers.result_classes import Register
from ....source_code_classes import Range, Diagnostic, Highlight
from ....utils import internal_error, assert_type, StringBuilder


class CSymbolTable:
    def __init__(self):
        self.m2c = {}
        self.c2m = {}

    def __setitem__(self, k, v):
        assert_type(k, (NFunDef, NVarDef, NLclVarDef, NParamDef))
        assert_type(v, str)

        if id(k) in self.m2c: internal_error()
        if v in self.c2m: internal_error()

        self.m2c[id(k)] = v
        self.c2m[v] = k

    def __getitem__(self, k):
        if isinstance(k, (NFunDef, NVarDef, NLclVarDef, NParamDef)):
            return self.m2c[id(k)]
        elif isinstance(k, str):
            return self.c2m[k]
        else: internal_error()


def autogen():
    return 'autogen_' + ''.join(random.choices(string.ascii_lowercase, k=32))


def process(gc):
    btru = gc.btru

    gc.e2ui = {} # e2i : enum to unsigned int
    for i, e in enumerate(list(set(btru.enums))):
        gc.e2ui[e] = i

    cst = CSymbolTable()

    def before(node):
        if not isinstance(node, (NFunDef, NVarDef, NLclVarDef, NParamDef)): return

        if isinstance(node, NFunDef):
            if node.keyword.text == 'interrupt':
                cst[node] = node.id.text
                return

        cst[node] = autogen()

    def after(node):
        pass
    btru.iter_tree(before, after)
    del before, after

    gc.cst = cst

    gc.sb.append_lines('/* Generation time: %s */\n' % datetime.datetime.now())
    gc.sb.append_lines('/* C to MCL Symbol Map:')
    gc.sb.indent()
    for cs, mo in cst.c2m.items():
        gc.sb.append_lines(
            "%s %s %s %s" % (
                cs + ' ' * (42 - len(cs)), 
                mo.id.text + ' ' * (40 - len(mo.id.text)),
                type(mo).__name__ + ' ' * ( 20 - len(type(mo).__name__)),
                mo.id.range
            )
        )
    gc.sb.outdent()
    gc.sb.append_lines('*/\n')
