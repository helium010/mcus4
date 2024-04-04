'''
Bind symbols defined in other modules.
'''


# pylint: disable=unused-wildcard-import

from ..Atributaries.modules.ast_classes import *
from ..Atributaries.registers.result_classes import Register
from ..source_code_classes import Range, Diagnostic, Highlight
from ..utils import internal_error


def process(btru):
    btru.successful = True

    global_syms = set()
    for reg in btru.registers:
        global_syms.add(
            reg.split('.')[0]
        )
    for mod in btru.modules:
        global_syms.add(
            mod.split('.')[0]
        )

    def before(node):
        if isinstance(node, NRef):
            if 'st' not in node.first.__dict__:
                if node.first.text in global_syms:

                    cr = node.first.text  # cr : current ref
                    ct = node.first  # ct : current token

                    fdrs = btru.fdrs
                    while True:
                        btru.hls.append(Highlight(
                            ct.range,
                            'namespace'
                        ))
                        ct.st = 'ns'
                        for fdr in fdrs.copy():
                            if not fdr.startswith(cr):
                                fdrs.remove(fdr)

                        # Nothing matched.
                        if len(fdrs) == 0:
                            btru.add_diag(
                                ct.range,
                                'Unexpected symbol.'
                            )
                            btru.successful = False
                            return

                        # One fdr matched.
                        elif len(fdrs) == 1 and list(fdrs)[0].split('.').__len__() == len(cr.split('.')):
                            fdr = list(fdrs)[0]

                            # If fdr != cr, it means cr is a 'nearly complete'
                            # reference except last symbol in fdr, such as
                            # 'flash.a' and 'flash.acr'.
                            # TODO: Add code completion here.
                            if fdr != cr:
                                btru.add_diag(
                                    ct.range,
                                    "Incomplete symbol.\nSymbol '%s' expected." % fdr.split('.')[-1]
                                )
                                btru.successful = False
                                return
                            obj = btru[fdr]
                            ct.object = obj
                            if isinstance(obj, Register):
                                _next = ct.next
                                if isinstance(_next, NSubTwo):
                                    btru.add_diag(
                                        _next.range,
                                        'Two expression subscription is not allowed for register.'
                                    )
                                    btru.successful = False
                                    return
                                if isinstance(_next, NSubOne):
                                    aie = _next.exp  # ae : address index expression
                                    if not isinstance(aie, NToken):
                                        btru.add_diag(
                                            aie.range,
                                            'Only immediate uint is allowed here.'
                                        )
                                        btru.successful = False
                                        return
                                    if aie.type != 'IMM_UINT':
                                        btru.add_diag(
                                            aie.range,
                                            'Only immediate uint is allowed here.'
                                        )
                                        btru.successful = False
                                        return
                                    btru.add_hlt(
                                        aie.range,
                                        'constant-other'
                                    )
                                    ai = int(aie.text)
                                    if ai >= len(obj.addresses):
                                        btru.add_diag(
                                            aie.range,
                                            "'%d' is not a valid address index (0 <= idx < %d )." % (ai, len(obj.addresses))
                                        )
                                        btru.successful = False
                                        return

                                    _next = _next.next
                                else:
                                    ai = 0

                                if _next is None:
                                    btru.add_diag(
                                        node.range,
                                        'Incomplete reference.\nField of register or subscription expected.'
                                    )
                                    btru.successful = False
                                    return
                                if not isinstance(_next, NToken):
                                    btru.add_diag(
                                        _next.range,
                                        "Field of register expected."
                                    )
                                    btru.successful = False
                                    return

                                btru.add_hlt(
                                    _next.range,
                                    'heading'
                                )
                                _next.ai = ai
                                fld_nm = _next.text
                                # Field doesn't exist. Maybe this is because
                                # user is just typing and field name is not
                                # complete.
                                if fld_nm not in obj:
                                    # TODO: Add code completion here.
                                    btru.add_diag(
                                        _next.range,
                                        "Register '%s' has no field '%s'" % (obj.dot_ref, fld_nm)
                                    )
                                    btru.successful = False
                                    return

                                fld = obj[fld_nm]
                                _next.st = 'fld'
                                _next.object = fld

                                _next = _next.next
                                if _next is not None:
                                    btru.add_diag(
                                        Range(_next.range, node.last.range),
                                        "No more items are allowed here."
                                    )
                                    btru.successful = False
                                    return
                            elif isinstance(obj, NMod):
                                _next = ct.next
                                if _next is None:
                                    btru.add_diag(
                                        node.range,
                                        'Incomplete reference.\nFunction or variable expected.'
                                    )
                                    btru.successful = False
                                    return
                                if _next.text not in obj:
                                    btru.add_diag(
                                        _next.range,
                                        "Symbol '%s' not defined" % _next.text
                                    )
                                    btru.successful = False
                                    return
                                obj = obj[_next.text]
                                _next.st = obj.id.st
                                _next.object = obj
                                if _next.st == 'function':
                                    btru.add_hlt(_next.range, 'function')

                                _next_sym = _next.next_symbol
                                if _next_sym is not None:
                                    btru.add_diag(
                                        Range(_next_sym.range, node.last.range),
                                        "No more symbol is allowed after type '%s'" % _next.st
                                    )
                                    btru.successful = False
                                    return
                            else: internal_error()

                            return

                        # Two or more fdrs matched.
                        else:

                            ct = ct.next
                            # If ct is None, then this ref is
                            # incomplete.
                            # TODO: Add code completion here.
                            if ct is None:
                                btru.add_diag(
                                    node.range,
                                    'incomplete reference'
                                )
                                btru.successful = False
                                break
                            cr = cr + '.' + ct.text

    def after(node):
        pass
    btru.iter_tree(before, after)
    del before, after
