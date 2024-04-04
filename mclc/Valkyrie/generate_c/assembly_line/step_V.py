'''
Generate main function.
'''

# pylint: disable=unused-wildcard-import
import random, string, datetime

from ....Atributaries.modules.ast_classes import *
from .pgfs import fun_def


def process(gc):
    btru = gc.btru

    init_stats = []
    mainloop_stats = []
    init_stats.extend(
        btru['system-init']
    )
    mainloop_stats.extend(
        btru['system-mainloop']
    )

    def before(node):
        if isinstance(node, NMod):
            for mi in node.mis:
                if isinstance(mi, NInit):
                    init_stats.extend(mi.stats)
                if isinstance(mi, NMainloop):
                    mainloop_stats.extend(mi.stats)


    def after(node):
        pass
    btru.iter_tree(before, after)
    del before, after



    gc.sb.append_lines("/* main function */")
    gc.sb.append_lines("int main()")
    gc.sb.append_lines("{")
    gc.sb.append_lines("")

    gc.sb.indent()
    gc.sb.append_lines("/* init */")
    gc.sb.append_lines("")
    from .pgfs import stt
    for init_stt in init_stats:

        gc.sb.append_lines(stt.gen(gc, init_stt))
    
    gc.sb.append_lines("")
    gc.sb.append_lines("")
    gc.sb.append_lines("/* mainloop */")
    gc.sb.append_lines("while (1)")
    gc.sb.append_lines("{")
    gc.sb.indent()
    for ml_stt in mainloop_stats:
        gc.sb.append_lines(stt.gen(gc, ml_stt))
    gc.sb.outdent()
    gc.sb.append_lines("}")
    gc.sb.outdent()
    gc.sb.append_lines("}")

    gc.sb.append_lines()
    gc.sb.append_lines("void SystemInit(){}")


