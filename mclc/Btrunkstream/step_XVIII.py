'''
Check types of function parameters.
'''

# pylint: disable=unused-wildcard-import

from ..Atributaries.modules.ast_classes import *
from ..Atributaries.registers.result_classes import Register
from ..source_code_classes import Range, Diagnostic, Highlight
from ..utils import internal_error

def process(btru):
    btru.successful = True
    def before(node):
        if isinstance(node, NFunCall):
            par_defs = node.ref.last.object.params
            pars = node.params

            if len(par_defs) != len(pars):
                btru.add_diag(
                    node.range,
                    "Number of arguments should be %d but not %d" % (
                        len(par_defs),
                        len(pars)
                    )
                )
                btru.successful = False
                return
            
            for pd, p in zip(par_defs, pars):
                if pd.type.st != p.it:
                    btru.add_diag(
                        p.range,
                        "Type '%s' is expected, but argument is of type '%s'." % (
                            pd.type.st,
                            p.it
                        )
                    )
                    btru.successful = False
                
                if pd.type.st == 'enum':
                    # enum value
                    ev = p.last.text 
                    # valid values
                    vvs = [tok.text for tok in pd.type.ids] 

                    if ev not in vvs:
                        btru.add_diag(
                            p.range,
                            "'%s' is not one of valid enum values {%s}" % (
                                ev,
                                ', '.join(["'%s'" % v for v in vvs])
                            )
                        )
                        btru.successful = False

                    
                
    def after(node):
        pass
    btru.iter_tree(before, after)
    del before, after