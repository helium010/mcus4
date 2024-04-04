'''
Find all symbols defined as enum value.
'''


# pylint: disable=unused-wildcard-import, function-redefined

from ..Atributaries.modules.ast_classes import *
from ..source_code_classes import Range, Diagnostic, Highlight
from . import ProcessError



def process(btru):
    btru.enums = []
    nodes_to_iter = []
    for mod in btru.modules.values():
        nodes_to_iter.append(mod)
    for blk in btru.blocks.values():
        nodes_to_iter.extend(blk)

    def before(node):
        if isinstance(node, NTEnum):
            btru.enums.extend([idt.text for idt in node.ids])
            for idt in node.ids:
                # hlt
                btru.hls.append(Highlight(
                    idt.range,
                    'constant-other'
                ))
                idt.st = 'enum-value'
    def after(node):
        pass
    for nd in nodes_to_iter:
        nd.iter_tree(before, after)
    del before, after

    btru.successful = True


    def before(node):
        if isinstance(node, NRef):
            first_sym = node.first.text
            if first_sym in btru.enums:

                # hlt
                btru.hls.append(Highlight(
                    node.first.range,
                    'constant-other'
                ))
                node.first.st = 'enum-value' # st : symbol type

                # diag
                if node.first.next is not None:
                    btru.add_diag(
                        node.first.next.range,
                        'Unexpected symbol after enum value.'
                    )
                    btru.successful = False
                


    def after(node):
        pass

    for nd in nodes_to_iter:
        nd.iter_tree(before, after)
    del before, after