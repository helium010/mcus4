'''
Check duplicated module symbol definitions.
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
                if sym not in sym_def_map:
                    sym_def_map[sym] = []
                sym_def_map[sym].append(mi.id)
        
        # dts : definition tokens
        for sym, dts in sym_def_map.items():
            if len(dts) > 1:
                for dt in dts:
                    btru.add_diag(
                        dt.range,
                        "Symbol '%s' defined multiple times." % sym
                    )
                btru.successful = True

                