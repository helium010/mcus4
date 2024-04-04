'''
Check duplicated local symbol definitions.

Local symbol can be:

1. Function parameter.
2. Variable defined in function.
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
                    [pd.id for pd in mi.params],
                    mi.stats
                ))

    btru.successful = True
    # pds : par_defs
    for par_toks, stats in scope_stats:
        sym_tok_map = {}
        for pt in par_toks:
            pts = pt.text
            if pts not in sym_tok_map:
                sym_tok_map[pts] = [pt]
            else:
                sym_tok_map[pts].append(pt)

        def before(node):
            nonlocal sym_tok_map
            if isinstance(node, NLclVarDef):
                st = node.id
                sts = st.text
                if sts not in sym_tok_map:
                    sym_tok_map[sts] = [st]
                else:
                    sym_tok_map[sts].append(st)

        def after(node):
            pass
        for stt in stats:
            stt.iter_tree(before, after)
        del before, after

        for sym, toks in sym_tok_map.items():
            if len(toks) > 1:
                for tk in toks:
                    btru.add_diag(
                        tk.range,
                        "Symbol '%s' defined multiple times." % sym
                    )
                btru.successful = False