from mclc.Atributaries.modules.lexcial_analyser import get_all_defined_tokens

print('all defined tokens:')
for tok in get_all_defined_tokens():
    tok_k = tok[0]
    tok_v = tok[1]
    print('    ' + str(tok_k) + ' ' * (40 - len(tok_k)) + str(tok_v))