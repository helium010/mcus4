from ...utils import error, internal_error


class Node:
    pass

    def __repr__(self):
        return type(self).__name__


class NToken(Node):
    def __init__(self, _type, text, _range):
        self.type = _type
        self.text = text
        self.range = _range

        # this field is used for ply.yacc
        # this is a temporary solution
        # remove if after replacing ply.yacc
        self.value = self

    def iter_tree(self, before, after):
        before(self)
        after(self)

    def copy(self):
        nt = NToken(self.type, self.text, self.range)
        if 'st' in self.__dict__:
            nt.st = self.st
        return nt

    def __repr__(self):
        range_str = str('%d,%d - %d,%d' % (
            self.range.sln,
            self.range.scol,
            self.range.eln,
            self.range.ecol,
        ))

        res = 'Tok( ' + self.type + ', ' + self.text.replace('\n', ' ')

        return res + ' , ' + range_str + ' )'


class NSubOne(Node):
    def __init__(self, exp):
        self.exp = exp

    def iter_tree(self, before, after):
        before(self)
        self.exp.iter_tree(before, after)
        after(self)

    def copy(self):
        ns =  self.__class__(self.exp.copy())
        ns.range = self.range
        return ns


class NSubTwo(Node):
    def __init__(self, left_exp=None, right_exp=None):
        self.left_exp = left_exp
        self.right_exp = right_exp

    def iter_tree(self, before, after):
        before(self)
        if self.left_exp is not None:
            self.left_exp.iter_tree(before, after)
        if self.right_exp is not None:
            self.right_exp.iter_tree(before, after)
        after(self)

    def copy(self):
        ns = self.__class__(
            None if self.left_exp is None else self.left_exp.copy(),
            None if self.right_exp is None else self.right_exp.copy(),
        )
        ns.range = self.range

        return ns


class NRef(Node):

    def __init__(self):
        self.items = []

    def iter_tree(self, before, after):
        before(self)
        for it in self.items:
            it.iter_tree(before, after)
        after(self)

    def copy(self):
        nr = self.__class__()
        nr.range = self.range
        for it in self.items:
            nr.items.append(it.copy())
        return nr


class NExpOpExp(Node):
    def __init__(self, exp1, op, exp2):
        self.exp1 = exp1
        self.op = op
        self.exp2 = exp2

    def iter_tree(self, before, after):
        before(self)
        self.exp1.iter_tree(before, after)
        self.op.iter_tree(before, after)
        self.exp2.iter_tree(before, after)
        after(self)

    def copy(self):
        neoe = self.__class__(
            self.exp1.copy(),
            self.op.copy(),
            self.exp2.copy()
        )
        neoe.range = self.range
        return neoe


class NRetStat(Node):
    def __init__(self, exp=None):
        self.exp = exp

    def iter_tree(self, before, after):
        before(self)
        if self.exp is not None:
            self.exp.iter_tree(before, after)
        after(self)

    def copy(self):
        nrs = self.__class__(
            None if self.exp is None else self.exp.copy()
        )
        nrs.range = self.range
        return nrs


class NFunCall(Node):
    def __init__(self, ref, params):
        self.ref = ref
        self.params = params

    def iter_tree(self, before, after):
        before(self)
        self.ref.iter_tree(before, after)
        for par in self.params:
            par.iter_tree(before, after)
        after(self)

    def copy(self):
        nps = []
        for par in self.params:
            nps.append(par.copy())
        nc = self.__class__(
            self.ref.copy(),
            nps
        )
        nc.range = self.range
        return nc


class NAsgn(Node):
    def __init__(self, left, op, exp):
        self.left = left
        self.op = op
        self.exp = exp

    def iter_tree(self, before, after):
        before(self)
        self.left.iter_tree(before, after)
        self.op.iter_tree(before, after)
        self.exp.iter_tree(before, after)
        after(self)

    def copy(self):
    
        return self.__class__(
            self.left.copy(),
            self.op.copy(),
            self.exp.copy()
        )


class NLclVarDef(Node):
    def __init__(self, _id, _type):
        self.id = _id
        self.type = _type

    def iter_tree(self, before, after):
        before(self)
        self.id.iter_tree(before, after)
        self.type.iter_tree(before, after)
        after(self)

    def copy(self):
        nl = self.__class__(
            self.id.copy(),
            self.type.copy(),
        )
        nl.range = self.range
        return nl


class NWhile(Node):
    def __init__(self, cond, stats):
        self.cond = cond
        self.stats = stats

    def iter_tree(self, before, after):
        before(self)
        self.cond.iter_tree(before, after)
        for stt in self.stats:
            stt.iter_tree(before, after)
        after(self)

    def copy(self):
        return self.__class__(
            self.cond.copy(),
            [stt.copy() for stt in self.stats]
        )
         


class NIf(Node):
    def __init__(self,cond_stats, _else):
        self.cond_stats = cond_stats
        self._else = _else

    def iter_tree(self, before, after):
        before(self)
        for cond, stats in self.cond_stats:
            cond.iter_tree(before, after)
            for stt in stats:
                stt.iter_tree(before, after)
        for stt in self._else:
            stt.iter_tree(before, after)
        after(self)

    def copy(self):
        return self.__class__(
            [(c.copy(), [stt.copy() for stt in stts]) for c, stts in self.cond_stats],
            [stt.copy() for stt in self._else]
        )


class NTEnum(Node):
    def __init__(self, ids):
        self.ids = ids
        self.st = 'enum'

    def iter_tree(self, before, after):
        before(self)
        for _id in self.ids:
            _id.iter_tree(before, after)
        after(self)

    def copy(self):
        nt =  self.__class__([_id.copy() for _id in self.ids])
        nt.range = self.range
        return nt

class NIMMBytes(Node):
    def __init__(self, bts):
        self.bts = bts

    def iter_tree(self, before, after):
        before(self)
        for bt in self.bts:
            bt.iter_tree(before, after)
        after(self)

    def copy(self):
        nibs = self.__class__([bt.copy() for bt in self.bts])
        nibs.range = self.range
        return nibs

class NInit(Node):
    def __init__(self, stats):
        self.stats = stats

    def iter_tree(self, before, after):
        before(self)
        for stt in self.stats:
            stt.iter_tree(before, after)
        after(self)

    def copy(self):
        return self.__class__([stt.copy() for stt in self.stats])


class NMainloop(Node):
    def __init__(self, stats):
        self.stats = stats

    def iter_tree(self, before, after):
        before(self)
        for stt in self.stats:
            stt.iter_tree(before, after)
        after(self)

    def copy(self):
        return self.__class__([stt.copy() for stt in self.stats])


class NMod(Node):
    def __init__(self, mis):
        self.mis = mis

    def iter_tree(self, before, after):
        before(self)
        for mi in self.mis:
            mi.iter_tree(before, after)
        after(self)

    def copy(self):
        return self.__class__([mi.copy() for mi in self.mis])

    def __contains__(self, k):
        for mi in self.mis:
            if 'id' in mi.__dict__:
                if mi.id.text == k:
                    return True
        return False
    
    def __getitem__(self, k):
        if not isinstance(k, str):
            raise TypeError
        if k not in self:
            raise KeyError

        for mi in self.mis:
            if 'id' in mi.__dict__:
                if mi.id.text == k:
                    return mi
        internal_error()

class NParamDef(Node):
    def __init__(self, _type, _id):
        self.type = _type
        self.id = _id

    def iter_tree(self, before, after):
        before(self)
        self.type.iter_tree(before, after)
        self.id.iter_tree(before, after)
        after(self)

    def copy(self):
        return self.__class__(self.type.copy(), self.id.copy())


class NFunDef(Node):
    def __init__(self, modifiers, keyword, _id, params, return_type, stats):
        self.modifiers = modifiers
        self.keyword = keyword
        self.id = _id
        self.params = params
        self.return_type = return_type
        self.stats = stats

        self.st = 'function'

    def iter_tree(self, before, after):
        before(self)
        for mod in self.modifiers:
            mod.iter_tree(before, after)
        self.id.iter_tree(before, after)
        for par in self.params:
            par.iter_tree(before, after)
        if self.return_type is not None:
            self.return_type.iter_tree(before, after)
        for stt in self.stats:
            stt.iter_tree(before, after)
        after(self)

    def copy(self):
        nf = self.__class__(
            [mod.copy() for mod in self.modifiers],
            self.keyword,
            self.id.copy(),
            [par.copy() for par in self.params],
            None if self.return_type is None else self.return_type.copy(),
            [stt.copy() for stt in self.stats]
        )
        nf.range = self.range
        return nf


class NVarDef(Node):
    def __init__(self, modifiers, _id, _type, init_value):
        self.modifiers = modifiers
        self.id = _id
        self.type = _type
        self.init_value = init_value

    def iter_tree(self, before, after):
        before(self)
        for mdfr in self.modifiers:
            mdfr.iter_tree(before, after)
        self.id.iter_tree(before, after)
        self.type.iter_tree(before, after)
        self.init_value.iter_tree(before, after)
        after(self)

    def copy(self):
        nv = self.__class__(
            [mod.copy() for mod in self.modifiers],
            self.id.copy(),
            self.type.copy(),
            self.init_value.copy()
        )
        nv.range = self.range
        return nv


for k, v in globals().copy().items():
    if type(v) == type:
        if issubclass(v, Node) and v != Node:
            node_name = v.__name__

            if not k.startswith('N'):
                error("class name of AST Node must start with 'N'")

            if 'copy' not in v.__dict__:
                error('copy of %s is not implemented' % node_name)

            if 'iter_tree' not in v.__dict__:
                error('iter_tree of %s is not implemented' % node_name)

# delete useless functions and variables
try:
    del k, v, node_name
except NameError:
    pass
