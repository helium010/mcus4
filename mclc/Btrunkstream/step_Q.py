'''
Bind symbols defined local.
'''

# pylint: disable=unused-wildcard-import

from ..Atributaries.modules.ast_classes import *
from ..source_code_classes import Range, Diagnostic, Highlight


def process(btru):
    scope_stats = []
    for blk in btru.blocks.values():

        scope_stats.append(({}, blk))
    for mod in btru.modules.values():
        for mi in mod.mis:
            if isinstance(mi, NFunDef):

                scope_stats.append((
                    mi.params,
                    mi.stats
                ))

    btru.successful = True

    # pds : par_defs
    for pds, stats in scope_stats:

        sym_def_map = {}
        for pd in pds:
            sym = pd.id.text
            sym_def_map[sym] = pd
            pd.id.object = pd
            pd.id.st = pd.type.st
            btru.hls.append(Highlight(
                pd.id.range,
                'parameter'
            ))

        def before(node):

            # check if this ref is local
            if isinstance(node, NRef):
                # if first of ref already has st
                if 'st' in node.first.__dict__:
                    # do nothing on this ref
                    return

                first_sym = node.first.text

                # if first of ref is defined local
                if first_sym in sym_def_map:
                    obj = sym_def_map[first_sym]
                    node.first.object = obj
                    node.first.st = obj.id.st

                    if node.first.next_symbol is not None:
                        btru.add_diag(
                            node.first.next_symbol.range,
                            'Unexpected symbol.'
                        )
                        btru.successful = False

            # add new defined local
            if isinstance(node, NLclVarDef):
                sym = node.id.text

                sym_def_map[sym] = node
                node.id.object = node
                node.id.st = node.type.st

        def after(node):
            pass

        for stt in stats:
            stt.iter_tree(before, after)
        del before, after


    
