# pylint: disable=unused-wildcard-import

from .ast_classes import *
from ...source_code_classes import Range, Diagnostic

from . import lexcial_analyser
tokens = [tok[0] for tok in lexcial_analyser.get_all_defined_tokens()]


def p_error(tok_and_context):
    tok = tok_and_context[0]
    context = tok_and_context[1]
    context: ParsingContext
    if tok:
        _range = tok.range
        tok_name = tok.type
    else:
        _range = Range(
            context.file_dot_ref,
            1 << 16,
            1 << 16
        )
        tok_name = 'EOF'
    context.diags.append(Diagnostic(
        _range,
        'Syntactic Analysing Error : Unexpected %s' % tok_name
    ))
    context.successful = False


class ParsingContext:
    def __init__(self, file_dot_ref):
        self.file_dot_ref = file_dot_ref
        self.diags = []
        self.successful = True


def _update_range(syms: list):
    first = syms[1]
    last = syms[len(syms) - 1]
    syms[0].range = Range(first.range, last.range)

# def p_wdtzncddvhzedvuebgvsrwugicgpjtpz(syms: list):
#     '''
#     temp : init NEWLINE
#     '''
#     syms[0] = syms[1]


def p_gybedzhbptohmtwuzxzxasofseniagtx(syms: list):
    '''
    module : zom_seps oom_mis oom_seps
           | zom_seps oom_mis
    '''
    syms[0] = NMod(syms[2])


def p_ewpmmtatxnhcykvtqkbhpdsjgcvsduix(syms: list):
    '''
    module : oom_seps
           | 
    '''
    syms[0] = NMod([])


def p_ozshipozsekgvdqeeewulmyqeavlikur(syms: list):
    '''
    oom_mis : oom_mis oom_seps mi 
    '''
    syms[0] = syms[1]
    syms[0].append(syms[3])


def p_rbqtnluabzdhnmtuqwcroggnsdrlwuzt(syms: list):
    '''
    oom_mis : mi
    '''
    syms[0] = [syms[1]]


def p_wseygdmvsmfuykimtkjxinmsmlcpphst(syms: list):
    '''
    mi : init
       | mainloop
       | fun_def
       | var_def
    '''
    syms[0] = syms[1]


def p_poqdhixfsuitblpyxyyciaqhaqsvsxsd(syms: list):
    '''
    var_def : mdfrs VAR ID COLON_ type EQUALS_SIGN_ immediate
    '''
    syms[0] = NVarDef(
        syms[1],
        syms[3],
        syms[5],
        syms[7]
    )
    if len(syms[1]) == 0:
        _update_range([syms[0]] + syms[2:])
    else:
        _update_range([syms[0]] + syms[1] + syms[2:])


def p_xsqobxakyiqdqhygvtmgztneykndgmgr(syms: list):
    '''
    fun_def : mdfrs fun_kwd ID LEFT_PARENTHESIS_ par_defs RIGHT_PARENTHESIS_ return_def zom_seps LEFT_CURLY_BRACKET_ zom_stats RIGHT_CURLY_BRACKET_
    '''
    syms[0] = NFunDef(
        syms[1],
        syms[2],
        syms[3],
        syms[5],
        syms[7],
        syms[10]
    )
    if len(syms[1]) == 0:
        _update_range([syms[0]] + syms[2:])
    else:
        _update_range([syms[0]] + syms[1] + syms[2:])


def p_vcwojxvmkbsqppdcvgitkozercbswyjj(syms: list):
    '''
    fun_kwd : FUN
            | INTERRUPT
    '''
    syms[0] = syms[1]


def p_ozjunrpatndvqbytuqxbewlutvynkzbt(syms: list):
    '''
    mdfrs : mdfrs mdfr
    '''
    syms[0] = syms[1]
    syms[0].append(syms[2])


def p_bvedzvwsfcusllrchqssjjfcchbdnxqg(syms: list):
    '''
    mdfrs : mdfr
          |
    '''
    syms[0] = syms[1:]


def p_hmvvuvghdxjhjdhnhbwrrmvnhiqvnioj(syms: list):
    '''
    mdfr : EXPORT
    '''
    syms[0] = syms[1]


def p_lhiphtunphaggttdflokxxgruvvgkeui(syms: list):
    '''
    par_defs :  
    '''
    syms[0] = []


def p_lrdbgkdawhssxldzzbmnqkbnhdcugvea(syms: list):
    '''
    par_defs : par_defs COMMA_ par_def
    '''
    syms[0] = syms[1]
    syms[0].append(syms[3])


def p_uepacqwuivzdqlctkkbevuktsrtcdims(syms: list):
    '''
    par_defs : par_def
    '''
    syms[0] = [syms[1]]


def p_dbqheruaxbeouqqitvfcpyfsydgaiavy(syms: list):
    '''
    par_def : ID COLON_ type
    '''
    syms[0] = NParamDef(syms[3], syms[1])


def p_hybxevydynvwptifsovukzmnyrherzkt(syms: list):
    '''
    return_def :
    '''
    syms[0] = None


def p_onuinsbzvzqgokfwsvteuhyyxxkehdjs(syms: list):
    '''
    return_def : COLON_ type
    '''
    syms[0] = syms[2]


def p_pyaxeswyirykohvqrouzcsmtohyncvtn(syms: list):
    '''
    mainloop : MAINLOOP zom_seps LEFT_CURLY_BRACKET_ zom_stats RIGHT_CURLY_BRACKET_
    '''
    syms[0] = NMainloop(syms[4])

    _update_range(syms)


def p_wofwtueujbjhthyarmmklgmcngudzgcp(syms: list):
    '''
    init : INIT zom_seps LEFT_CURLY_BRACKET_ zom_stats RIGHT_CURLY_BRACKET_
    '''
    syms[0] = NInit(syms[4])

    _update_range(syms)


def p_dtzrsheswwbfzouswofjzzjwnfllbruu(syms: list):
    '''
    zom_stats : oom_seps soss oom_seps
    zom_stats : oom_seps soss
    '''
    syms[0] = syms[2]


def p_fedwebrzysktcdprzypvakulitdeqaga(syms: list):
    '''
    zom_stats : soss oom_seps
    '''
    syms[0] = syms[1]


def p_bobnhggspzmkgeouptlbwknzqfuztyvi(syms: list):
    '''
    zom_stats : oom_seps
              |
    '''
    syms[0] = []


def p_dyqduclqqxftbibjszngtehqxxablyno(syms: list):
    '''
    soss : soss oom_seps statement 
    '''
    syms[0] = syms[1]
    syms[0].append(syms[3])


def p_zjsejawjhifslymdwlukfgkbqzdxjrvl(syms: list):
    '''
    soss : statement
    '''
    syms[0] = [syms[1]]


def p_cjslcxrlgsxsdtyhyzadvwqipkeyxxez(syms: list):
    '''
    statement : assignment
              | function_call
              | flow_control
              | return_stat
    '''
    syms[0] = syms[1]



def p_coinbztlzkwpwhrvrgvimkzdwrwxqwfy(syms: list):
    '''
    flow_control : if
                 | while
    '''
    syms[0] = syms[1]


def p_rhvfvsjmouhgntepmosyskukxcplgpgp(syms: list):
    '''
    while : WHILE exp_t
    '''
    syms[0] = NWhile(
        syms[2],
        []
    )


def p_lepvngzxmdjioholrjmmwtkxrvwqnfln(syms: list):
    '''
    while : WHILE exp_t LEFT_CURLY_BRACKET_ zom_stats RIGHT_CURLY_BRACKET_
    '''
    syms[0] = NWhile(
        syms[2],
        syms[4]
    )


def p_bgvaoxjqjgbqmnkafwlsyeiomibwpvkc(syms: list):
    '''
    if : if_if
    '''
    syms[0] = NIf(
        [syms[1]],
        []
    )


def p_gzklplwoijktahcqhhjiihrjpywyzmjj(syms: list):
    '''
    if : if_if if_else
    '''
    syms[0] = NIf(
        [syms[1]],
        syms[2]
    )


def p_otpbqjvluchmdrzogpqzyrawtrlitxdi(syms: list):
    '''
    if : if_if if_elifs
    '''
    syms[0] = NIf(
        [syms[1]] + syms[2],
        []
    )


def p_gylfqamhzjkflgnmborkwiwlcwblqkmq(syms: list):
    '''
    if : if_if if_elifs if_else
    '''
    syms[0] = NIf(
        [syms[1]] + syms[2],
        syms[3]
    )


def p_yeggqevhswmbskkvxqaswtuqpwjpnrts(syms: list):
    '''
    if_elifs : if_elifs if_elif
    '''
    syms[0] = syms[1]
    syms[0].append(syms[2])


def p_izogprpuucwphfknvzoghsfedcnqzffb(syms: list):
    '''
    if_elifs : if_elif
    '''
    syms[0] = [syms[1]]


def p_mxlkiwmiikvkduaqapxyuihlhfywuijk(syms: list):
    '''
    if_if   : IF   exp_t LEFT_CURLY_BRACKET_ zom_stats RIGHT_CURLY_BRACKET_
    if_elif : ELIF exp_t LEFT_CURLY_BRACKET_ zom_stats RIGHT_CURLY_BRACKET_
    '''
    syms[0] = (syms[2], syms[4])


def p_rocoefgcdhuwpcffrxtgmgrufaygzbqt(syms: list):
    '''
    if_else : ELSE LEFT_CURLY_BRACKET_ zom_stats RIGHT_CURLY_BRACKET_ 
    '''
    syms[0] = syms[3]


def p_mvkqmjxrmqjhrtgrwdjpxsaaikomxqmv(syms: list):
    '''
    assignment : asgn_left EQUALS_SIGN_ exp_t
                | asgn_left PLUS_SIGN_EQUALS_SIGN_ exp_t
                | asgn_left HYPHEN_MINUS_EQUALS_SIGN_ exp_t
                | asgn_left AMPERSAND_EQUALS_SIGN_ exp_t
                | asgn_left VERTICAL_LINE_EQUALS_SIGN_ exp_t
    '''
    syms[0] = NAsgn(
        syms[1],
        syms[2],
        syms[3],
    )
    _update_range(syms)


def p_hsgwkmpbkdlqdrfpjtphkzgynnfsoecr(syms: list):
    '''
    asgn_left : reference
    '''
    syms[0] = syms[1]


def p_lgkmttnpcyklmuafycxbutgdgijykrgz(syms: list):
    '''
    asgn_left : VAR ID COLON_ type 
    '''
    syms[0] = NLclVarDef(
        syms[2],
        syms[4]
    )
    _update_range(syms)


def p_bumkcrqrdoovbigffghprvzqgcohwvlg(syms: list):
    '''
    function_call : reference LEFT_PARENTHESIS_ exp_comma_list RIGHT_PARENTHESIS_
    '''
    syms[0] = NFunCall(syms[1], syms[3])
    _update_range(syms)


def p_ofsskejmmxbgesjfcmdousxgruhaqafo(syms: list):
    '''
    exp_comma_list : exp_comma_list COMMA_ exp_t
    '''
    syms[0] = syms[1]
    syms[0].append(syms[3])


def p_wnolhaoxyjgmovclhlglccanahnwspfo(syms: list):
    '''
    exp_comma_list : exp_t
    '''
    syms[0] = [syms[1]]


def p_htvpikgybzffuhtzvgbvxwszprsqsdro(syms: list):
    '''
    exp_comma_list : 
    '''
    syms[0] = []


def p_kpbhyihlsefivowrrjakesbnxomkqrir(syms: list):
    '''
    return_stat : RETURN exp_t
    '''
    syms[0] = NRetStat(syms[2])

    _update_range(syms)


def p_xkushjcnemvnllzjevvfrcyodwpwqcrg(syms: list):
    '''
    return_stat : RETURN
    '''
    syms[0] = NRetStat()

    _update_range(syms)


def p_lipaetnypurnlurysnznbvnnzghllzxn(syms: list):
    '''
    exp_4 : exp_4 AND exp_3
            | exp_4 OR exp_3
    exp_3 : exp_3 LESS_THAN_SIGN_ exp_2
            | exp_3 GREATER_THAN_SIGN_ exp_2
            | exp_3 LESS_THAN_SIGN_EQUALS_SIGN_ exp_2
            | exp_3 GREATER_THAN_SIGN_EQUALS_SIGN_ exp_2
            | exp_3 EQUALS_SIGN_EQUALS_SIGN_ exp_2
            | exp_3 EXCLAMATION_MARK_EQUALS_SIGN_ exp_2
    exp_2 : exp_2 PLUS_SIGN_ exp_1
            | exp_2 HYPHEN_MINUS_ exp_1
    exp_1 : exp_1 ASTERISK_ exp_0
            | exp_1 SOLIDUS_ exp_0
    '''
    syms[0] = NExpOpExp(
        syms[1],
        syms[2],
        syms[3]
    )

    _update_range(syms)


def p_wexlkcrxfdchhweiduwrjqeywzoozizs(syms: list):
    '''
    exp_t     : exp_4
    exp_4     : exp_3
    exp_3     : exp_2
    exp_2     : exp_1
    exp_1     : exp_0
    exp_0     : reference
              | function_call
              | immediate
    immediate : IMM_UINT
              | IMM_BYTE
              | IMM_INT
              | IMM_HEX
              | IMM_BIN
              | IMM_STRING
              | IMM_MEMORY
              | IMM_BOOL
              | IMM_BYTES
              | IMM_UINTS
              | imm_byte_array
    '''
    syms[0] = syms[1]


def p_gmmnobwllpltfbhwyrxyjagcyryhhjpd(syms: list):
    '''
    imm_byte_array : LEFT_CURLY_BRACKET_ zom_seps ibs zom_seps RIGHT_CURLY_BRACKET_
    '''
    syms[0] = NIMMBytes(syms[3])

    _update_range(syms)


def p_qdtafmytfeyygimmarkxyylkccmutbvb(syms: list):
    '''
    ibs : ibs zom_seps IMM_BYTE COMMA_ 
    '''
    syms[0] = syms[1]
    syms[0].append(syms[3])


def p_pnciwjkdsfnjxegpretzasbicpvngkyg(syms: list):
    '''
    ibs : IMM_BYTE COMMA_ 
    '''
    syms[0] = [syms[1]]


def p_rerxxambcdwlkrlbnfyxmarwububzsos(syms: list):
    '''
    exp_0 : LEFT_PARENTHESIS_ exp_t RIGHT_PARENTHESIS_
    '''
    syms[0] = syms[2]

    _update_range(syms)


def p_lptiitpoamfylhjkoidebkbornatimrk(syms: list):
    # id.id
    '''
    reference : reference FULL_STOP_ ID
    '''
    ref = syms[1]
    item = syms[3]
    ref.items.append(item)
    syms[0] = ref

    _update_range(syms)


def p_fngdswmhedeqfqxhnrmowjjzypyecvpc(syms: list):
    # id[0:1]
    '''
    reference : reference LEFT_SQUARE_BRACKET_ exp_t COLON_ exp_t RIGHT_SQUARE_BRACKET_
    '''
    ref = syms[1]
    item = NSubTwo(syms[3], syms[5])
    item.range = Range(syms[2].range, syms[6].range)
    ref.items.append(item)
    syms[0] = ref

    _update_range(syms)


def p_ysovoadiawkfclbthfutozvmrvuvmxnx(syms: list):
    # id[:1]
    '''
    reference : reference LEFT_SQUARE_BRACKET_ COLON_ exp_t RIGHT_SQUARE_BRACKET_
    '''
    ref = syms[1]
    item = NSubTwo(right_exp=syms[4])
    item.range = Range(syms[2].range, syms[5].range)
    ref.items.append(item)
    syms[0] = ref

    _update_range(syms)


def p_kglyyreiweyaatntphgputhkvvjayorj(syms: list):
    # id[0:]
    '''
    reference : reference LEFT_SQUARE_BRACKET_ exp_t COLON_ RIGHT_SQUARE_BRACKET_
    '''
    ref = syms[1]
    item = NSubTwo(left_exp=syms[3])
    item.range = Range(syms[2].range, syms[5].range)
    ref.items.append(item)
    syms[0] = ref

    _update_range(syms)


def p_aaxbymqgqkotnxpxhibbzmswtdevzwso(syms: list):
    # id[0]
    '''
    reference : reference LEFT_SQUARE_BRACKET_ exp_t RIGHT_SQUARE_BRACKET_
    '''
    ref = syms[1]
    item = NSubOne(syms[3])
    item.range = Range(syms[2].range, syms[4].range)
    ref.items.append(item)
    syms[0] = ref

    _update_range(syms)


def p_jyjvhvfhxpqvrgwzmrxsrtkccgshpcdo(syms: list):
    # id
    '''
    reference : ID
    '''
    ref = NRef()
    ref.items.append(syms[1])
    syms[0] = ref

    _update_range(syms)


def p_abcgneyyqltfycghpetqaamwjankyqri(syms: list):
    '''
    type : UINT
         | UINTS
         | INT
         | BYTES
         | BYTE
         | BOOL
    '''
    syms[0] = syms[1]
    syms[0].st = syms[1].text


def p_qiastzdcmppsgwrttebvqvqjrqossocs(syms: list):
    '''
    type : ENUM LEFT_CURLY_BRACKET_ id_comma_list RIGHT_CURLY_BRACKET_
    '''
    syms[0] = NTEnum(syms[3])

    _update_range(syms)


def p_ggrhuoqchrtituwilljohnmmetsoxfbc(syms: list):
    '''
    id_comma_list : id_comma_list COMMA_ ID
    '''
    syms[0] = syms[1]
    syms[0].append(syms[3])


def p_gtecttjlltditcwvzuialpeecdgixhid(syms: list):
    '''
    id_comma_list : ID 
    '''
    syms[0] = [syms[1]]


def p_dwtrtwtyuneyxuqvxmxfyvdnlauehrgk(syms: list):
    '''
    id_comma_list : 
    '''
    syms[0] = []


def p_zchpprfvahukivqsibzpvitqrwqgmwoo(syms: list):
    '''
    zom_seps : SEPS
             |
    oom_seps : SEPS
    '''
