from types import FunctionType
import re

def error(msg: str=''):
    print('\x1b[31m[ ERROR ]\x1b[0m %s\n' % str(msg))
    breakpoint()
    raise Exception()

def internal_error():
    error('internal error')

def print_warning(msg:str):
    print('\x1b[35m[WARNING]\x1b[0m %s' % str(msg))

def print_ok(msg:str):
    print('\x1b[32m[  O K  ]\x1b[0m %s' % str(msg))

def print_error(msg:str):
    print('\x1b[31m[ ERROR ]\x1b[0m %s' % str(msg))

def assert_type(ins, _type, msg=''):
    msg = ' : ' + msg if msg != '' else ''
    if not isinstance(ins, _type):
        error('Type of %s is not %s%s' % (ins, _type, msg))


def indent_lines_str(lines_str:str):
    new_lines = indent_lines(lines_str.splitlines())
    return '\n'.join(new_lines)

def indent_lines(lines:[]):
    new_lines = []
    for line in lines:
        new_lines.append('    ' + line)
    return new_lines


def is_str_uint(s:str):
    return re.match(r'0x\d+', s) or re.match(r'\d+', s)

def is_str_str(s:str):
    return re.match(r"'[^']*'", s)

import inflect

inflect_engine = inflect.engine()

def add_prefix_to_each_line(block: str, prefix: str) -> str:
    new_block = ''
    lines = block.splitlines(keepends=True)
    for line in lines:
        new_block += prefix + line

    return new_block

class StringBuilder():
    def __init__(self):
        self.code_str = ''
        self._indent = 0

    def append_lines(self, lines: str = '',):

        lines = add_prefix_to_each_line(lines, ' ' * self._indent)
        self.code_str = self.code_str + lines + '\n'

    def indent(self):
        self._indent += 4

    def outdent(self):
        if self._indent - 4 < 0:
            error('Cannot outdent beyond outermost')
        self._indent -= 4

    def build(self) -> str:

        return self.code_str
    
    def remove_empty_lines(self):
        new_str = ''
        for l in self.code_str.splitlines():
            if l.strip() != '':
                new_str += l + '\n'
        self.code_str = new_str



def is_valid_p(p):
    if not p.exists():
        return False

    from . import context
    if p in context.blks.values():
        return True
    
    if p.name.endswith(('.mcl', '.reg')):
        return True



def dot_ref_from_path(p):

    from . import context
    if p in context.blks.values():
        for fdr, bp in context.blks.items():
            if p == bp:
                return fdr
    

    if not p.name.endswith(('.mcl', '.reg')):
        error('internal error')

    return p.relative_to(context.src_dir).as_posix().replace('/', '.')[:-4]

def is_valid_fdr(dr):
    from . import context
    if dr in context.blks:
        return True
        
    path_str_base = dr.replace('.', '/')
    pr = context.src_dir.joinpath(path_str_base + '.reg')
    pm = context.src_dir.joinpath(path_str_base + '.mcl')

    if pr.exists() and pm.exists():
        error('internal error')
    if pr.exists():
        return True
    elif pm.exists():
        return True
    else:
        return False

def path_from_dot_ref(dr):

    from . import context
    if dr in context.blks:
        return context.blks[dr]

    path_str_base = dr.replace('.', '/')

    pr = context.src_dir.joinpath(path_str_base + '.reg').absolute()
    pm = context.src_dir.joinpath(path_str_base + '.mcl').absolute()

    if pr.exists() and pm.exists():
        error('internal error')
    if pr.exists():
        return pr
    elif pm.exists():
        return pm
    else:
        error('internal error')