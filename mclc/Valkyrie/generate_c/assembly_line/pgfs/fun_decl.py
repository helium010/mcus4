from .....utils import StringBuilder, internal_error
from . import mt2ct


def t2c(t):

    if t is None:
        rts = 'void'
    else:
        rtt = t.st
        if rtt in mt2ct:
            rts = mt2ct[rtt]
        elif rtt == 'enum':
            rts = 'volatile unsigned int'
        elif rtt == 'bytes':
            rts = 'volatile unsigned char *'
        elif rtt == 'uints':
            rts = 'volatile unsigned int *'
        else: internal_error()
    return rts


def gen(gc, fun_def):
    # sb : string builder
    sb = StringBuilder()
    sb.append_lines(
        "/* function declartion : '%s' in '%s' */" % (fun_def.id.text, fun_def.id.range)
    )
    cs = gc.cst[fun_def]

    sb.append_lines(
        "%s %s(%s);" % (
            t2c(fun_def.return_type),
            cs,
            ', '.join(
                [t2c(pd.type) for pd in fun_def.params]
            )
        )
    )

    return sb.build()
