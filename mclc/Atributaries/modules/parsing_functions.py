from .lexcial_analyser import construct_tokens_from_text
from .syntactic_analyser import construct_AST_from_tokens



def parse_mod_file(file_dot_ref, file_text, mod_type='mcl'):
    diags = []

    successful, tokens, _diags = construct_tokens_from_text(file_dot_ref, file_text)
    diags.extend(_diags)
    if not successful:
        return False, None, diags

    successful, ast, _diags = construct_AST_from_tokens(file_dot_ref, tokens, mod_type)
    diags.extend(_diags)

    if not successful:
        return False, ast, diags
    
    return successful, ast, diags
