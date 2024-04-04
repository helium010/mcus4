import re
from ...utils import error, internal_error
from ...source_code_classes import Range, Diagnostic
from .result_classes import RToken, Register, ExtraInfo, Field
from . import defined_extra_infos, defined_types

defined_lines = {
    'name': [
        r'.+'
    ],
    'address': [
        r'[\dx:\*\+ a-fA-F]+'
    ],
    'extra-infos': [
        '',
        '',
        r'\S+'
    ],
    'type': [
        r'\w+'
    ],
    'field': [
        r'\w+',  # field name
        r'[\d:]+',  # bit range
        '',  # the following regexes are optional
        r'\w+',  # type
        '',  # the following regex can be used multiple times
        r'\S+'  # extra data
    ]
}

for k, v in defined_lines.items():
    nv = []
    for r in v:
        if r != '':
            nv.append(re.compile(r))
        else:
            nv.append('')
    defined_lines[k] = nv

del k, v, nv


class ParsingErrorException(Exception):
    pass


class ParsingSucceedException(Exception):
    pass


def parse_reg_file(file_dot_ref, file_text):

    diags = []
    reg = Register()

    def skip_spaces():
        nonlocal col
        while col < len(line_text):
            if line_text[col] == ' ':
                col += 1
            else:
                break

    def parsing_error(*args):

        if len(args) == 1:
            diags.append(Diagnostic(
                Range(
                    file_dot_ref,
                    ln, col, len(line_text)
                ),
                args[0]
            ))
        elif len(args) == 2:
            diags.append(Diagnostic(
                args[0],
                args[1]
            ))
        else:
            internal_error()
        raise ParsingErrorException

    try:
        for ln, line_text in enumerate(file_text.splitlines()):
            # skip empty lines
            if line_text.strip() == '':
                continue

            col = 0
            # skip leading spaces
            skip_spaces()

            # try to match keyword of each defined line
            matched_key = None
            for key in defined_lines:
                if line_text[col:].startswith(key + ' '):
                    matched_key = key
            del key
            if matched_key is None:
                parsing_error("one of [%s] expected" % ', '.join(defined_lines))

            col += len(matched_key)

            token_regexes = defined_lines[matched_key]
            once_match_regexes = []
            optional_match_regexes = []
            repeatable_match_regex = None
            current_state = 'once'

            for tok_regex in token_regexes:
                if tok_regex == '':
                    if current_state == 'once':
                        current_state = 'optional'
                    elif current_state == 'optional':
                        current_state = 'repeatable'
                    continue
                if current_state == 'once':
                    once_match_regexes.append(tok_regex)
                elif current_state == 'optional':
                    optional_match_regexes.append(tok_regex)
                else:
                    repeatable_match_regex = tok_regex

            matched_tokens = []
            # match once_match_regexes
            for optional_regex in once_match_regexes:
                skip_spaces()

                mr = optional_regex.match(line_text[col:])

                # nothing match
                # parsing failed
                if mr is None:
                    parsing_error(
                        'once regular expression %s matching expected' % optional_regex.pattern
                    )
                matched_str = mr[0]
                tok = RToken(matched_str, Range(
                    file_dot_ref,
                    ln,
                    col,
                    col + len(matched_str)
                ))
                matched_tokens.append(tok)
                col += len(matched_str)

            # match optional_match_regexes
            for optional_regex in optional_match_regexes:
                skip_spaces()

                # no more chars
                if col == len(line_text):
                    # stop matching optional regexes
                    break

                mr = optional_regex.match(line_text[col:])

                # nothing match
                # parsing failed
                if mr is None:
                    parsing_error(
                        'optional regular expression %s matching expected' % optional_regex.pattern
                    )

                matched_str = mr[0]
                tok = RToken(matched_str, Range(
                    file_dot_ref,
                    ln,
                    col,
                    col + len(matched_str)
                ))
                matched_tokens.append(tok)
                col += len(matched_str)

            # match repeatable_match_regex
            if repeatable_match_regex is not None and col < len(line_text):
                while col < len(line_text):
                    skip_spaces()
                    mr = repeatable_match_regex.match(line_text[col:])
                    if mr is None:
                        break

                    matched_str = mr[0]
                    tok = RToken(matched_str, Range(
                        file_dot_ref,
                        ln,
                        col,
                        col + len(matched_str)
                    ))
                    matched_tokens.append(tok)
                    col += len(matched_str)

            skip_spaces()
            # no more text should appear
            if col < len(line_text):
                parsing_error('no more text should appear')

            if matched_key == 'name':
                reg.name = matched_tokens[0].text
                reg.name_range = matched_tokens[0].range

            if matched_key == 'address':
                addr_str = matched_tokens[0].text
                addr_tok_range = matched_tokens[0].range

                # parse address string
                if not addr_str.__contains__(':'):
                    addr_str = addr_str + ':0:1'
                addr_part_strs = addr_str.split(':')

                if len(addr_part_strs) != 3:
                    parsing_error(
                        addr_tok_range,
                        "number of ':' must be either 0 or 2"
                    )

                addr_current_col = addr_tok_range.scol
                base_addr_str = addr_part_strs[0]

                try:
                    base_addr = 0
                    for factor_str in base_addr_str.split('+'):
                        base_addr += int(factor_str, base=0)
                except ValueError:
                    parsing_error(
                        Range(
                            file_dot_ref,
                            ln,
                            addr_current_col,
                            addr_current_col + len(base_addr_str)
                        ),
                        'base address is not valid'
                    )

                addr_current_col += len(base_addr_str) + 1
                step_length_str = addr_part_strs[1]
                try:
                    step_length = int(step_length_str, base=0)
                except ValueError:
                    parsing_error(
                        Range(
                            file_dot_ref,
                            ln,
                            addr_current_col,
                            addr_current_col + len(step_length_str)
                        ),
                        'step length is not valid'
                    )
                addr_current_col += len(step_length_str) + 1
                step_times_str = addr_part_strs[2]
                try:
                    step_times = int(step_times_str, base=0)
                except ValueError:
                    parsing_error(
                        Range(
                            file_dot_ref,
                            ln,
                            addr_current_col,
                            addr_current_col + len(step_times_str)
                        ),
                        'step times not valid'
                    )

                addrs = []
                for i in range(step_times):
                    addrs.append(base_addr + step_length * i)

                reg.addresses.extend(addrs)
                reg.address_ranges.append(matched_tokens[0].range)

            if matched_key == 'type':
                reg.type = matched_tokens[0].text
                reg.type_range = matched_tokens[0].range
                if reg.type not in defined_types:
                    parsing_error(
                        reg.type_range,
                        "Type '%s' is not defined." % reg.type
                    )

            if matched_key == 'extra-infos':
                for tok in matched_tokens:
                    if tok.text.__contains__('='):
                        k, v = tok.text.split('=', 1)
                    else:
                        k = tok.text
                        v = None
                    r = tok.range
                    if k not in defined_extra_infos:
                        parsing_error(
                            r,
                            'key is not defined'
                        )
                    reg.extra_infos.append(ExtraInfo(
                        k, v, r
                    ))

            if matched_key == 'field':

                # name
                field = Field()
                reg.fields.append(field)
                field.name = matched_tokens[0].text
                field.name_range = matched_tokens[0].range

                # bits
                bits_str = matched_tokens[1].text
                if not bits_str.__contains__(':'):
                    bits_str = bits_str + ':' + bits_str
                left, right = bits_str.split(':', 1)
                try:
                    left = int(left)
                    right = int(right)
                except ValueError:
                    parsing_error(
                        matched_tokens[1].range,
                        'not a valid bit range'
                    )
                field.bits = (left, right)
                field.bits_range = matched_tokens[1].range

                if len(matched_tokens) >= 3:
                    field.type = matched_tokens[2].text
                    field.type_range = matched_tokens[2].range
                    if field.type not in defined_types:
                        parsing_error(
                            field.type_range,
                            "Type '%s' is not defined." % field.type
                        )

                    for tok in matched_tokens[3:]:
                        if tok.text.__contains__('='):
                            k, v = tok.text.split('=', 1)
                        else:
                            k = tok.text
                            v = None
                        r = tok.range
                        if k not in defined_extra_infos:
                            parsing_error(
                                r,
                                'key is not defined'
                            )
                        field.extra_infos.append(ExtraInfo(
                            k, v, r
                        ))

        if len(reg.addresses) == 0:
            parsing_error(
                Range(file_dot_ref, 0, 0, 1, 0),
                'address not defined'
            )
        
        if reg.type is None:
            for fld in reg.fields:
                if fld.type is None:
                    parsing_error(
                        Range(
                            fld.name_range.file_dot_ref,
                            fld.name_range.sln,
                            0,
                            fld.name_range.sln,
                            1 << 16,
                        ),
                        "Type of field is not defined."
                    )


    except ParsingErrorException:
        return False, reg, diags

    return True, reg, diags
