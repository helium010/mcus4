import unicodedata, re

from ...utils import error
from ...source_code_classes import Range, Diagnostic
from .ast_classes import NToken

# pragma token definitions
literal_chars = (
    '+', '-', '*', '/',
    '++', '--',
    '=', '+=', '-=', '&=', '|=',
    '<', '>', '<=', '>=', '==', '!=',
    '(', ')', '[', ']', '{', '}',

    ':',
    '->',

    '.',

    ',',

    ' ',
    ';',
)

keyword_tokens = (
    'interrupt',
    'export',
    'fun',
    'init',
    'mainloop',

    
    'return',

    'while',
    'if',
    'elif',
    'else',

    'and',
    'or',
    'not',

    'var',

    'uint',
    'uints',
    'int',
    'bytes',
    'byte',
    'bool',

    'enum',
)


regex_tokens = {
    'IMM_STRING': r"'[^']*'",
    'IMM_UINT': r'[1-9]\d*|0',
    'IMM_BYTE': r'0x[0-9a-fA-F]+bt|0b[01]+bt|([1-9]\d*|0)bt',
    'IMM_INT': r'-?([1-9]\d*|0)s',
    'IMM_UINTS': r'([1-9]\d*|0)uints',
    'IMM_BYTES': r'([1-9]\d*|0)bytes|0x[0-9a-fA-F]+bytes',
    'IMM_MEMORY' : r'0x[0-9a-fA-F]+memory\d+',
    'IMM_HEX': r'0x[0-9a-fA-F]+',
    'IMM_BIN': r'0b[01]+',
    'IMM_BOOL' : r'true|false',
    'ID': r'[a-zA-Z_][0-9a-zA-Z_]*',
    'COMMENT': r'\#.*',
    'NEWLINE': r'\n'
}

special_tokens = (
    'SEPS',
)


# pragma parsing token definitions
literal_map = {}
regex_map = {}

literal_char_names = []
keyword_token_names = []


for chars in literal_chars:
    k = ''
    for c in chars:
        k += unicodedata.name(c).replace(' ', '_').replace('-', '_')
        k += '_'
    v = chars
    if literal_map.__contains__(k):
        error()
    literal_map[k] = v
    literal_char_names.append(k)

for keyword in keyword_tokens:
    k = keyword.upper()
    v = keyword
    if literal_map.__contains__(k):
        error("Token %r multiply defined" % k)
    literal_map[k] = v
    keyword_token_names.append(k)

regex_map.update(regex_tokens)

# compile regex
for t, r in regex_map.items():
    regex_map[t] = re.compile(r)


def get_all_defined_tokens():
    toks = []
    toks.extend(literal_map.items())
    toks.extend(regex_map.items())
    for st in special_tokens:
        toks.append((st, None))
    return toks


class LexicalAnalysingSucceedException(Exception):
    pass


class LexicalAnalysingFailedException(Exception):
    pass


def construct_tokens_from_text(file_dot_ref, mod_text):
    '''
    return : is_successful, tokens, diags
    '''

    tokens = []
    diags = []
    ln = 0
    col = 0

    # Add a NEWLINE to end of file to prevent strange bug.
    # The reason of adding a NEWLINE solving this bug is unknown.
    # This is a temporary solution and still has potential risks.
    # TODO: Find the reason of this bug and use a reasonable 
    # method to fix it.
    mod_text += '\n'

    lines = mod_text.splitlines()
    eofln = 0 if (len(lines) == 0) else len(lines) - 1
    eofcol = 0 if (len(lines) == 0) else len(lines[-1])
    del lines

    try:
        while True:
            if len(mod_text) == 0:
                raise LexicalAnalysingSucceedException

            # find all matches
            matchs = []
            # literal_map
            for k, v in literal_map.items():
                if mod_text.startswith(v):
                    matchs.append((k, v))

            # regex_map
            for k, pattern in regex_map.items():
                match = pattern.match(mod_text)
                if match:
                    matchs.append([k, match[0]])

            # find the longest match
            max_len = 0
            match = None
            for _match in matchs:
                v = _match[1]
                if max_len < len(v):
                    max_len = len(v)
                    match = _match

            # check if has at least one match
            if match is None:
                raise LexicalAnalysingFailedException('Lexical Analysing Error : unexpected characters')
            del _match

            # mark start position
            start_pos = (ln, col)

            # update `ln` and `col` to
            # end of this token
            if match[0] == 'NEWLINE':
                ln += 1
                col = 0
            else:
                col += max_len

            # remove processed text
            mod_text = mod_text[max_len:]

            # construct token
            tokens.append(NToken(
                match[0], 
                match[1],
                Range(file_dot_ref, *start_pos, ln, col)
            ))

    except LexicalAnalysingFailedException as e:
        diags.append(Diagnostic(
            Range(file_dot_ref, ln, col, eofln, eofcol),
            e.args[0]
        ))

        return False, tokens, diags

    except LexicalAnalysingSucceedException:
        tts = []
        sep_toks = []
        for tok in tokens:
            if tok.type in ('SPACE_', 'NEWLINE', 'SEMICOLON_', 'COMMENT'):
                sep_toks.append(tok)
            else:
                if len(sep_toks) != 0:
                    ts = [t.type for t in sep_toks]
                    if 'NEWLINE' in ts or 'SEMICOLON_' in ts:
                        tts.append(NToken('SEPS',' ', Range(sep_toks[0].range, sep_toks[-1].range)))
                    sep_toks.clear()
                tts.append(tok)
        tokens = tts
        return True, tokens, diags

    return False, tokens, diags