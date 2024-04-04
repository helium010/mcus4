from ..utils import internal_error
from ..source_code_classes import Diagnostic, Highlight


class Btru:
    def __init__(self, atri):
        self.blocks = atri.blocks
        self.modules = atri.modules
        self.registers = atri.registers
        self.diags = atri.diags
        self.hls = []

        self.successful = atri.successful

    def iter_tree(self, before, after):
        tops = []
        for blk in self.blocks.values():
            tops.extend(blk)
        tops.extend(self.modules.values())
        for top in tops:
            top.iter_tree(before, after)

    # fdrs : file_dot_refs
    @property
    def fdrs(self):
        rs = set()
        for r in self.modules:
            rs.add(r)
        for r in self.registers:
            rs.add(r)
        return rs

    def __contains__(self, k):
        if not isinstance(k, str): raise TypeError

        if k in self.registers: return True

        if k in self.modules: return True

        if k in self.blocks: return True

        else: return False

    def __getitem__(self, k):
        if not isinstance(k, str):
            raise TypeError

        if k not in self:
            raise KeyError

        for fdr, obj in self.registers.items():
            if fdr == k:
                return obj
        for fdr, obj in self.modules.items():
            if fdr == k:
                return obj

        for fdr, obj in self.blocks.items():
            if fdr == k:
                return obj

        internal_error()

    def add_diag(self, _range, msg):
        import traceback as tb
        fr = tb.extract_stack()[-2]
        caller_file_name = fr.filename.split('/')[-1]
        ln = fr.lineno

        self.diags.append(Diagnostic(
            _range,
            msg,
            source=caller_file_name + ':' + str(ln)
        ))

    def add_hlt(self, _range, _type):
        self.hls.append(Highlight(_range, _type))
