'''
Check types of subscriptions.
'''

# pylint: disable=unused-wildcard-import

from ..Atributaries.modules.ast_classes import *
from ..Atributaries.registers.result_classes import Register
from ..source_code_classes import Range, Diagnostic, Highlight
from ..utils import internal_error

def process(btru):
    btru.successful = True
    ses = [] # ses : subscription expressions
    def before(node):
        nonlocal ses
        if isinstance(node, NSubOne):
            ses.append(node.exp)
        if isinstance(node, NSubTwo):
            if node.left_exp is not None:
                ses.append(node.left_exp)
            if node.right_exp is not None:
                ses.append(node.right_exp)
            if isinstance(node.previous.object, NParamDef):
                if node.right_exp is None:
                    btru.add_diag(
                        node.range,
                        "Upper bound of subscription of bytes defined as parameter can't be empty."
                    )
                    btru.successful = False

    def after(node):
        pass
    btru.iter_tree(before, after)
    del before, after

    for se in ses:
        if se.it != 'uint':
            btru.add_diag(
                se.range,
                "Type '%s' is not allowed for subscription." % se.it
            )
            btru.successful = False
