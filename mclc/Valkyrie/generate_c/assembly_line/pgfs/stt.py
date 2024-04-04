# pylint: disable=unused-wildcard-import
from .....Atributaries.modules.ast_classes import *
from .mask import bitmask
from .....utils import StringBuilder


def gen(gc, stt):
    if isinstance(stt, NAsgn):
        from . import exp

        # lst : left symbol type

        vd = False  # vd : variable definition
        if isinstance(stt.left, NLclVarDef):
            lst = stt.left.type.text
            vd = True
        elif isinstance(stt.left.last, NSubOne):
            lst = 'subone'
        elif isinstance(stt.left.last, NSubTwo):
            lst = 'subtwo'

        elif isinstance(stt.left, NRef):
            lst = stt.left.last.st
        else:
            internal_error()

        if not vd:
            if lst == 'fld':
                ref = stt.left
                return write_field(ref, exp.gen(gc, stt.exp))
            elif lst in ['byte', 'uint', 'int', 'bool']:
                return gc.cst[stt.left.last.object] + ' ' + stt.op.text + ' ' + exp.gen(gc, stt.exp) + ';'
            elif lst == 'subone':
                return "%s[%s] = %s;" % (
                    gc.cst[stt.left.last.previous.object],
                    exp.gen(gc, stt.left.last.exp),
                    exp.gen(gc, stt.exp)
                )

            elif lst in ['subtwo', 'bytes']:
                raise NotImplementedError
            elif lst == 'enum':
                raise NotImplementedError
            else: internal_error()
        else:
            if lst == 'byte':
                return 'unsigned char ' + gc.cst[stt.left.id.object] + ' ' + stt.op.text + ' ' + exp.gen(gc, stt.exp) + ';'
            elif lst == 'uint':
                return 'unsigned int ' + gc.cst[stt.left.id.object] + ' ' + stt.op.text + ' ' + exp.gen(gc, stt.exp) + ';'
            else:
                raise NotImplementedError

    elif isinstance(stt, NWhile):
        return gen_while(gc, stt)
    elif isinstance(stt, NIf):
        return gen_if(gc, stt)
    elif isinstance(stt, NFunCall):
        from . import fun_call
        return fun_call.gen(gc, stt) + ';'
    elif isinstance(stt, NRetStat):
        if stt.exp is None:
            return 'return;'
        else:
            from . import exp
            return 'return %s;' % exp.gen(gc, stt.exp)
    else: internal_error()


def write_field(ref, exp_str):
    fld_sym = ref.last
    ai = fld_sym.ai
    fld = fld_sym.object
    reg = fld.reg

    addr = reg.addresses[ai]

    default_type = reg.type

    awa_flds = []  # awa : always write as
    war_flds = []  # war ; write as read

    class Stop(Exception): pass
    for f in reg.fields:
        if f is fld:
            continue
        try:
            for ei in f.extra_infos:
                if ei.key == 'always-write-as':
                    awa_flds.append((
                        f,
                        int(ei.value, base=0)
                    ))
                    raise Stop
                else: error("Not implemented extra-info key '%s'.") % ei.key
            if f.type is not None:
                ft = f.type
            elif default_type is not None:
                ft = default_type
            else: internal_error()

            if ft in ['rw']:
                war_flds.append(f)
            elif ft in ['w', 'r', 't']:
                awa_flds.append((
                    f, 0
                ))
            elif ft in ['rc_w0']:
                awa_flds.append((
                    f, 1
                ))
            else: error("Type '%s' is not implemented." % ft)
        except Stop: pass

    fvs = None  # fvs : field value str
    if fld.type is not None:
        ft = fld.type
    elif default_type is not None:
        ft = default_type
    else: internal_error()
    if ft in ['rw', 'w', 'rc_w0']:
        fvs = '((%s) << %du)' % (
            exp_str,
            fld.bits[1]
        )
    elif ft in ['r']:
        fvs = '0'
    elif ft == 't':
        fvs = '(%s ^ ((%s) << %du))' % (
            '(%s & %s)' % (
                '(*((volatile unsigned int *) %#.8Xu))' % addr,
                '%#Xu' % (bitmask(fld.bits)),
            ),
            exp_str,
            fld.bits[1]
        )

    # warvs : write as read value str
    warvs = '((*((volatile unsigned int *) %#.8Xu)) & %#xu)' % (
        addr,
        bitmask(*[f.bits for f in war_flds])
    )

    # awav : always write as value
    awav = 0
    for awaf, awafv in awa_flds:
        awav |= awafv << awaf.bits[1]

    # ofvs : other fields value str
    ofvs = '( %s | %#xu )' % (
        warvs,
        awav
    )

    comment = '/* write field %s of %s */' % (fld.name, reg.dot_ref)
    return comment + '\n' + '%s = %s | %s;\n' % (
        '(*((volatile unsigned int *) %#.8Xu))' % addr,
        fvs,
        ofvs
    )


def gen_while(gc, stt):
    from . import exp
    sb = StringBuilder()
    sb.append_lines(
        "while (%s)" % exp.gen(gc, stt.cond)
    )
    sb.append_lines("{")
    sb.indent()
    for wstt in stt.stats:
        sb.append_lines(
            gen(gc, wstt)
        )
    sb.outdent()
    sb.append_lines("}")
    return sb.build()


def gen_if(gc, stt):
    from . import exp
    sb = StringBuilder()
    for i, cs in enumerate(stt.cond_stats):
        if i == 0:
            sb.append_lines(
                "if (%s)" % exp.gen(gc, cs[0])
            )
        else:
            sb.append_lines(
                "else if (%s)" % exp.gen(gc, cs[0])
            )
        sb.append_lines("{")
        sb.indent()
        for wstt in cs[1]:
            sb.append_lines(
                gen(gc, wstt)
            )
        sb.outdent()
        sb.append_lines("}")
    sb.append_lines('else')
    sb.append_lines('{')
    sb.indent()
    for es in stt._else:
        sb.append_lines(
            gen(gc, es)
        )
    sb.outdent()
    sb.append_lines('}')

    return sb.build()
