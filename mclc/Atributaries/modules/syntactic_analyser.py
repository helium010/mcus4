from ...utils import print_error, error
from . import yacc
from . import grammar
from .grammar import ParsingContext


defualt_enabled_logging = (
    # 'debug',
    # 'info',
    # 'warning',
    # 'error',
    'critical'
)


class PLYLogger(object):

    def __init__(self, enabled=None):
        self.enabled = enabled if enabled else defualt_enabled_logging

    def debug(self, msg, *args, **kwargs):
        if 'debug' in self.enabled:
            print((msg % args))

    def info(self, msg, *args, **kwargs):
        if 'info' in self.enabled:
            print((msg % args))

    def warning(self, msg, *args, **kwargs):
        if 'warning' in self.enabled:
            print((msg % args))

    def error(self, msg, *args, **kwargs):
        if 'error' in self.enabled:
            print((msg % args))

    def critical(self, msg, *args, **kwargs):
        if 'critical' in self.enabled:
            print((msg % args))


mcl_parser = yacc.yacc(
    module=grammar,
    debug=False,
    write_tables=False,
    debuglog=PLYLogger(),
    errorlog=PLYLogger()
)



blk_parser = yacc.yacc(
    module=grammar,
    debug=False,
    write_tables=False,
    debuglog=PLYLogger(),
    errorlog=PLYLogger(),
    start='zom_stats'
)




def construct_AST_from_tokens(file_dot_ref, tokens, mod_type='mcl'):
    '''
    return : successful, ast, diags
    '''

    if mod_type == 'mcl':
        parser = mcl_parser
    elif mod_type == 'blk':
        parser = blk_parser
    else:
        error('mod_type must be either mcl or blk')


    # next_token
    i = 0

    def next_token():
        nonlocal i
        if i < tokens.__len__():
            tok = tokens[i]
            i += 1
            return tok
        else:
            return None

    # parse
    parsing_context = ParsingContext(file_dot_ref)
    res = parser.parse(
        parsing_context,
        tokenfunc=next_token,
        debug_logger=PLYLogger([]),
    )

    if parsing_context.successful:
        return True, res, parsing_context.diags
    else:
        return False, res, parsing_context.diags
