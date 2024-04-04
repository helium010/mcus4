'''
Bind symbols defined in same module.
'''


# pylint: disable=unused-wildcard-import

from ..Atributaries.modules.ast_classes import *
from ..source_code_classes import Range, Diagnostic, Highlight


def process(btru):

    btru.successful = True
    for mod in btru.modules.values():
        sym_def_map = {} 
        for mi in mod.mis:
            if isinstance(mi, (NFunDef, NVarDef)):
                sym = mi.id.text
                sym_def_map[sym] = mi
                mi.id.object = mi
                if isinstance(mi, NVarDef):
                    mi.id.st = mi.type.st
                else:
                    btru.add_hlt(
                        mi.id.range,
                        'function'
                    )
                    mi.id.st = mi.st
        
        def before(node):

            # check if this ref is local
            if isinstance(node, NRef):
                # if first of ref already has st
                if 'st' in node.first.__dict__:
                    # do nothing on this ref
                    return

                first_sym = node.first.text
                if first_sym in sym_def_map:
                    obj = sym_def_map[first_sym]
                    node.first.object = obj
                    node.first.st = obj.id.st

                    if obj.id.st == 'function':
                        btru.add_hlt(
                            node.first.range,
                            'function'
                        )

                    if node.first.next_symbol is not None:
                        btru.add_diag(
                            node.first.next_symbol.range,
                            "No more items are allowed here."
                        )
                        btru.successful = False

        def after(node):
            pass
        mod.iter_tree(before, after)
        del before, after
        