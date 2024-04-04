import time
from pathlib import Path

from ..utils import error, print_error, dot_ref_from_path
from .. import context
from .result_classes import Atri





class BlkUnit:
    def __init__(self, path):
        self.path = path

        self._cached_text = None
        self._cached_result = None

    def process(self):
        new_text = self.path.read_text()

        # if content of file didn't change since last processing
        if new_text == self._cached_text:
            return self.commit_result()

        self._cached_text = new_text

        from .modules import parsing_functions
        successful, ast, diags = parsing_functions.parse_mod_file(self.path.name, new_text, 'blk')
        self._cached_result = (successful, ast, diags)

        return self.commit_result()

    def commit_result(self):
        successful, ast, diags = self._cached_result
        nds = [d.copy() for d in diags]

        if not successful:
            return False, None, nds
        from .modules.post_processor import post_process_ast
        na = post_process_ast(ast)

        return successful, na, nds


class MclUnit:
    def __init__(self, path):
        self.path = path

        self._cached_text = None
        self._cached_result = None

    @property
    def dot_ref(self):
        return dot_ref_from_path(self.path)

    def process(self):
        new_text = self.path.read_text()

        # if content of file didn't change since last processing
        if new_text == self._cached_text:
            return self.commit_result()

        self._cached_text = new_text

        from .modules import parsing_functions
        successful, ast, diags = parsing_functions.parse_mod_file(self.dot_ref, new_text)
        self._cached_result = (successful, ast, diags)

        return self.commit_result()

    def commit_result(self):
        successful, ast, diags = self._cached_result
        nds = [d.copy() for d in diags]

        if not successful:
            return False, None, nds
        from .modules.post_processor import post_process_ast
        na = post_process_ast(ast)
        na.fdr = self.dot_ref

        return successful, na, nds


class RegUnit:
    def __init__(self, path):
        self.path = path

        self._cached_text = None

        self._cached_result = None

    @property
    def dot_ref(self):
        return dot_ref_from_path(self.path)

    def process(self):
        new_text = self.path.read_text()

        # if content of file didn't change since last processing
        if new_text == self._cached_text:
            return self.commit_result()

        self._cached_text = new_text

        from .registers import parsing_functions
        successful, reg, diags = parsing_functions.parse_reg_file(
            self.dot_ref,
            new_text
        )
        self._cached_result = (successful, reg, diags)

        return self.commit_result()

    def commit_result(self):
        '''
        Copy reg and diags.

        Do some post process.
        '''
        successful, reg, diags = self._cached_result
        if not successful:
            return False, None, [d.copy() for d in diags]

        nr = reg.copy()
        nds = [d.copy() for d in diags]
        nr.dot_ref = self.dot_ref
        for fld in nr.fields:
            fld.reg = nr
            for ei in fld.extra_infos:
                ei.field = fld
                ei.reg = nr
        for ei in nr.extra_infos:
            ei.field = None
            ei.reg = nr
        return successful, nr, nds


from ..context import blks
blk_units = {}

for fdr, p in blks.items():
    blk_units[fdr] = BlkUnit(p)

mcl_units = {}
reg_units = {}


def update_units():
    global mcl_units, reg_units

    # remove units of unexisting files
    # drs : dot refs
    drs = set()
    # fp : file path
    for fp in list(context.src_dir.glob('**/*.mcl')) + list(context.src_dir.glob('**/*.reg')):
        dr = dot_ref_from_path(fp)
        for odr in drs:  # odr : other dot ref
            if dr.startswith(odr) or odr.startswith(dr):
                error("ref '%s' of %s is conflict with ref '%s'" % (dr, fp, odr))
        drs.add(dr)

    # udr : unit dot ref
    for udr in mcl_units.copy():
        if udr not in drs:
            mcl_units.pop(udr)

    for udr in reg_units.copy():
        if udr not in drs:
            reg_units.pop(udr)

    # add new units
    for fp in context.src_dir.glob('**/*.mcl'):
        dr = dot_ref_from_path(fp)
        if dr not in mcl_units:
            mcl_units[dr] = MclUnit(fp)

    for fp in context.src_dir.glob('**/*.reg'):
        dr = dot_ref_from_path(fp)
        if dr not in reg_units:
            reg_units[dr] = RegUnit(fp)


def process():

    update_units()

    atri = Atri()

    atri.successful = True
    for ref, u in reg_units.items():
        successful, reg, diags = u.process()
        atri.successful &= successful
        atri.registers[ref] = reg
        atri.diags.extend(diags)

    for ref, u in mcl_units.items():
        successful, ast, diags = u.process()
        atri.successful &= successful
        atri.modules[ref] = ast
        atri.diags.extend(diags)

    for ref, u in blk_units.items():
        successful, ast, diags = u.process()
        atri.successful &= successful
        atri.blocks[ref] = ast
        atri.diags.extend(diags)

    return atri
