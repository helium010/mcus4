'''
Check types of function returns.
'''

# pylint: disable=unused-wildcard-import

from ..Atributaries.modules.ast_classes import *
from ..Atributaries.registers.result_classes import Register
from ..source_code_classes import Range, Diagnostic, Highlight
from ..utils import internal_error


def process(btru):
    btru.successful = True
    for mod in btru.modules.values():
        for mi in mod.mis:
            if isinstance(mi, NFunDef):
                rt = mi.return_type
                has_ret = False

                def before(node):
                    nonlocal rt, has_ret 
                    if isinstance(node, NRetStat):
                        has_ret = True
                        if rt is None and node.exp is None:
                            return
                        if rt is None:
                            btru.add_diag(
                                node.range,
                                "Function should return 'void'."
                            )
                            btru.successful = False
                            return
                        if node.exp is None:
                            btru.add_diag(
                                node.range,
                                "Function should return '%s'." % rt.st
                            )
                            btru.successful = False
                            return
                        if rt.st != node.exp.it:
                            btru.add_diag(
                                node.range,
                                "Function should return '%s' but not '%s'" % (rt.st, node.exp.it)
                            )
                            btru.successful = False
                            return
                        
                def after(node):
                    pass
                for stt in mi.stats:
                    stt.iter_tree(before, after)
                del before, after

                if rt is not None and not has_ret:
                    btru.add_diag(
                        rt.range,
                        "Function has no return statement."
                    )
                    btru.successful = False
