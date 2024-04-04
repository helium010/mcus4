# pylint: disable=unsupported-membership-test,unsubscriptable-object,unused-wildcard-import

from ..Atributaries.modules.ast_classes import *
from ..Atributaries.registers.result_classes import Field, Register
from ..source_code_classes import Range
from .. import context


def definition_object_range_from_position(fdr, ln, col):
    if fdr not in context.btru:
        return None

    obj = context.btru[fdr]

    if not isinstance(obj, (NMod, list)):
        return None

    mdr = None  # mr : matched definition range

    def before(node):
        if not isinstance(node, NToken): return
        if (ln, col) not in node.range: return
        if 'object' not in node.__dict__: return

        nonlocal mdr
        obj = node.object
        if isinstance(obj, Register):
            mdr = Range(obj.dot_ref, 0, 0)
        if isinstance(obj, Field):
            mdr = obj.name_range
        if isinstance(obj, NMod):
            mdr = Range(obj.fdr, 0, 0)
        if isinstance(obj, NFunDef):
            mdr = obj.id.range
        if isinstance(obj, NVarDef):
            mdr = obj.id.range
        if isinstance(obj, NParamDef):
            mdr = obj.id.range
        if isinstance(obj, NLclVarDef):
            mdr = obj.id.range

    def after(node):
        pass
    if isinstance(obj, NMod):
        obj.iter_tree(before, after)
    else:
        for n in obj:
            n.iter_tree(before, after)
    del before, after

    return mdr

def fld_object_from_position(fdr, ln, col):
    if fdr not in context.btru:
        return None
    obj = context.btru[fdr]

    for fld in obj.fields:
        if (ln, col) in fld.name_range:
            return fld
        

    return None