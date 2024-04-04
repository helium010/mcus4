'''
Check types of assignments.
'''

# pylint: disable=unused-wildcard-import

from ..Atributaries.modules.ast_classes import *
from ..Atributaries.registers.result_classes import Register
from ..source_code_classes import Range, Diagnostic, Highlight
from ..utils import internal_error


def process(btru):
    btru.successful = True

    def before(node):
        if isinstance(node, NAsgn):

            if node.left.it == 'enum':
                btru.add_diag(
                    node.left.range,
                    "Type enum is not assignable."
                )
                btru.successful = False
                return

            if node.left.it != node.exp.it:
                if node.left.it != 'uint' or node.exp.it != 'byte':
                    btru.add_diag(
                        node.op.range,
                        "Type '%s' can't be assigned to type '%s'." % (
                            node.exp.it,
                            node.left.it
                        )
                    )
                    btru.successful = False
                    return

            # Check assignments for registers' fields.
            if isinstance(node.left, NRef):
                if 'st' not in node.left.last.__dict__: return
                if node.left.last.st != 'fld': return
                if node.op.text != '=':
                    btru.add_diag(
                        node.op.range,
                        "Assignment '%s' is not valid for register's field." % node.op.text
                    )
                    btru.successful = False
                    return
                if 'iv' in node.exp.__dict__:
                    if not node.left.last.object.is_valid_value(node.exp.iv):
                        btru.add_diag(
                            node.op.range,
                            "Value '%d' is not valid for field '%s' (0 <= v < %d)" % (
                                node.exp.iv,
                                node.left.last.object.name,
                                node.left.last.object.value_bound
                            )
                        )
                        btru.successful = False
                        return

    def after(node):
        pass
    btru.iter_tree(before, after)
    del before, after
