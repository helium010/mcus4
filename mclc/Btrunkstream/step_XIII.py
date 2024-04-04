'''
Infer types of expressions.
'''

# pylint: disable=unused-wildcard-import

from ..Atributaries.modules.ast_classes import *
from ..Atributaries.registers.result_classes import Register
from ..source_code_classes import Range, Diagnostic, Highlight
from ..utils import internal_error


it_rules = [
    (['+', '-', '*', '/'],
        'A', ['byte', 'uint', 'int']),
    (['>', '<', '>=', '<='],
        'B', ('byte', 'uint', 'int'), 'bool'),
    (['==', '!='],
        'C', ('byte', 'uint', 'int'), ('bool', ), ('enum', ), 'bool'),
    (['and', 'or'],
        'D', ('bool',), 'bool')
]

iv_rules = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a // b,
}

class Stop(Exception):
    pass

def process(btru):
    btru.successful = True

    try:

        some_change = True
        while some_change:
            some_change = False

            def before(node):
                if not isinstance(node, NExpOpExp): return

                nonlocal some_change
                # If node already has 'it', do nothing.
                if 'it' in node.__dict__: return
                # If any of node's children has no 'it', do nothing
                if 'it' not in node.exp1.__dict__ or 'it' not in node.exp2.__dict__: return

                ot = node.op.text  # ot : operator text
                mr = None  # mr : matched rule
                for r in it_rules:
                    if ot in r[0]: mr = r
                if mr is None: internal_error()
                rt = mr[1]  # rt : rule type
                if rt == 'A':
                    actps = mr[2]  # actps : acceptable types
                    mi = 0  # max index of type
                    for e in [node.exp1, node.exp2]:
                        if e.it not in actps:
                            btru.add_diag(
                                Range(e.range, node.op.range),
                                "Type '%s' is not supported for '%s'" % (e.it, ot)
                            )
                            raise Stop
                        mi = max(mi, actps.index(e.it))
                    node.it = actps[mi]
                    some_change = True
                    if ot not in iv_rules: return
                    if any(['iv' not in e.__dict__ for e in [node.exp1, node.exp2]]): return
                    iv_lambda = iv_rules[ot]
                    node.iv = iv_lambda(node.exp1.iv, node.exp2.iv)
                    return

                elif rt == 'B':
                    actps = mr[2]  # actps : acceptable types
                    for e in [node.exp1, node.exp2]:
                        if e.it not in actps:
                            btru.add_diag(
                                Range(e.range, node.op.range),
                                "Type '%s' is not supported for '%s'" % (e.it, ot)
                            )
                            raise Stop
                    node.it = mr[3]
                    some_change = True
                    return

                elif rt == 'C':
                    actps_grps = mr[2:5]  # actps_grp : acceptable types groups
                    for actps in actps_grps:
                        if all([e.it in actps for e in [node.exp1, node.exp2]]):
                            node.it = mr[5]
                            some_change = True
                            return
                    btru.add_diag(
                        node.range,
                        "Type '%s' and '%s' is not supported for '%s'" % (
                            node.exp1.it,
                            node.exp2.it,
                            ot
                        )
                    )
                    raise Stop

                elif rt == 'D':
                
                    if all([e.it == 'bool' for e in [node.exp1, node.exp2]]):
                        node.it = mr[3]
                        some_change = True
                        return
                    btru.add_diag(
                        node.range,
                        "Type '%s' and '%s' is not supported for '%s'" % (
                            node.exp1.it,
                            node.exp2.it,
                            ot
                        )
                    )
                    raise Stop

                else: internal_error()

            def after(node):
                pass
            btru.iter_tree(before, after)
            del before, after

    except Stop:
        btru.successful = False