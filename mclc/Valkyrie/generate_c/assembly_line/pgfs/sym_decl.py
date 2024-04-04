from .....utils import StringBuilder, internal_error
from . import mt2ct


def gen(gc, sym_def):
    # sb : string builder
    sb = StringBuilder()
    sb.append_lines(
        "/* variable declartion : '%s : %s' in '%s' */" % (sym_def.id.text, sym_def.type.text, sym_def.id.range)
    )
    cs = gc.cst[sym_def]  # cs : c symbol
    tt = sym_def.type.text  # tt : type text
    if tt in mt2ct:
        # ivt : initial value text
        ivt = str(sym_def.init_value.iv)

        sb.append_lines(
            "%s %s = %s;" % (mt2ct[tt], cs, ivt)
        )
    elif tt == 'bool':
        ivt = '1' if sym_def.init_value.iv else '0'
        sb.append_lines(
            "volatile unsigned char %s = %s;" % (cs, ivt)
        )
    elif tt == 'bytes':
        # iv : initial value
        iv = sym_def.init_value.iv
        if 'addr' not in sym_def.init_value.__dict__:
            if iv.count(0) == len(iv):
                sb.append_lines(
                    "volatile unsigned char %s[%d];" % (
                        cs, len(iv)
                    )
                )
            else:
                ivt = '{' + ', '.join([str(bv) for bv in iv ]) + '}'
                sb.append_lines(
                    "volatile unsigned char %s[] = %s;" % (
                        cs, ivt
                    )
                )
        else:
            sb.append_lines(
                "volatile unsigned char * %s = (volatile unsigned char *)%#.8Xu;" % (
                    cs,
                    sym_def.init_value.addr
                )
            )
    elif tt == 'uints' :
        if 'addr' not in sym_def.init_value.__dict__:
                sb.append_lines(
                    "volatile unsigned int %s[%d];" % (
                        cs, sym_def.init_value.ul
                    )
                )
        else:
            sb.append_lines(
                "volatile unsigned int * %s = (volatile unsigned int *)%#.8Xu;" % (
                    cs,
                    sym_def.init_value.addr
                )
            )

    else: internal_error()
    return sb.build()
