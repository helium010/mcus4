# pylint: disable=unused-wildcard-import
from .....Atributaries.modules.ast_classes import *
from .....Atributaries.registers.result_classes import *
from .....utils import StringBuilder
from .mask import bitmask


def gen(gc, exp):
    if isinstance(exp, NRef):
        if isinstance(exp.last, NToken):
            if isinstance(exp.last.object, Field):
                return field_read(gc, exp)
            return gc.cst[exp.last.object]
        elif isinstance(exp.last, NSubOne):
            from . import exp as eg
            return gc.cst[exp.last.previous.object] + '[%s]' % eg.gen(gc, exp.last.exp)
        else: raise NotImplementedError

    elif isinstance(exp, NExpOpExp):
        # opt : op text
        opt = exp.op.text
        if opt == 'and': opt = '&&'
        if opt == 'or': opt = '||'

        return "(%s %s %s)" % (
            gen(gc, exp.exp1),
            opt,
            gen(gc, exp.exp2)
        )
    elif isinstance(exp, NFunCall):
        from . import fun_call
        return fun_call.gen(gc, exp)
    elif isinstance(exp, NToken):
        return gen_imm(gc, exp)
    else:
        internal_error()


def field_read(gc, exp):
    ai = exp.last.ai
    fld = exp.last.object
    reg = fld.reg
    addr = reg.addresses[ai]
    return "%s (((*((volatile unsigned int *) %#.8Xu)) & %#xu) >> %du)" % (
        "/* read field %s of %s */" % (
            fld.name,
            reg.dot_ref
        ),
        addr,
        bitmask(fld.bits),
        fld.bits[1]
    )


def gen_imm(gc, imm):
    if imm.it in ['byte', 'uint', ]:
        return "%d" % imm.iv
    elif imm.it == 'int':
        return "%d" % imm.iv
    elif imm.it == 'bool':
        return '1' if imm.iv else '0'
    else:
        internal_error()
    return '/* this is an immediate operand */ 0'
