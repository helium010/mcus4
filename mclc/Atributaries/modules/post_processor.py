# pylint: disable=unused-wildcard-import, function-redefined
from .ast_classes import *
from ...utils import internal_error


def post_process_ast(ast):
    if isinstance(ast, NMod):
        nast = ast.copy()
        
    elif isinstance(ast, list):
        nast = [n.copy() for n in ast]
    else:
        internal_error()
    del ast

    def before(node):
        if isinstance(node, NRef):
            node.first = node.items[0]
            node.last = node.items[-1]

            for it in node.items:
                it.ref = node

            previous = None
            for it in node.items:
                it.previous = previous
                previous = it

            _next = None
            next_symbol = None
            for it in reversed(node.items):
                it.next = _next
                it.next_symbol = next_symbol
                _next = it
                if isinstance(it, NToken):
                    next_symbol = it

            for it in reversed(node.items):
                if isinstance(it, NToken):
                    node.last_symbol = it
                    break

        
    def after(node):
        pass
    if isinstance(nast, list):
        for stt in nast:
            stt.iter_tree(before, after)
    else:
        nast.iter_tree(before, after)
    del before, after

    return nast