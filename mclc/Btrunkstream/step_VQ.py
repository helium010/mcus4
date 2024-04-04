'''
Infer types of refs.
'''

# pylint: disable=unused-wildcard-import

from ..Atributaries.modules.ast_classes import *
from ..Atributaries.registers.result_classes import Register
from ..source_code_classes import Range, Diagnostic, Highlight
from ..utils import internal_error


def process(btru):
    btru.successful = True

    def before(node):
        if isinstance(node, NRef):
            last = node.last
            if isinstance(last, NToken):
                # it : inferred type
                if last.st == 'fld':
                    node.it = 'uint'
                elif last.st == 'function':
                    node.it = 'function'
                elif last.st == 'enum-value':
                    node.it = 'enum'
                elif last.st in [
                    'uint',
                    'uints',
                    'int',
                    'bytes',
                    'byte',
                    'bool',
                    'enum',
                ]:
                    node.it = last.st
                else:
                    internal_error()
            
            elif isinstance(last, (NSubOne, NSubTwo)):
                last_sym = node.last_symbol
                if last_sym.st not in  ['bytes', 'uints']:
                    btru.add_diag(
                        Range(last_sym.next.range, last.range),
                        "No subscription is allowed for type '%s'." % last_sym.st
                    )
                    btru.successful = False
                    return

                if last_sym.next != last:
                    btru.add_diag(
                        Range(last_sym.next.next.range, last.range),
                        "Only one subscription is allowed for type bytes"
                    )
                    btru.successful = False
                    return
                
                if isinstance(last, NSubOne):
                    if last_sym.st == 'bytes':
                        node.it = 'byte'
                    elif last_sym.st == 'uints':
                        node.it = 'uint'
                    else: internal_error()
                        
                else:
                    if last_sym.st == 'bytes':
                        node.it = 'bytes'
                    else: internal_error()
                
            else:
                internal_error()

    def after(node):
        pass
    btru.iter_tree(before, after)
    del before, after
