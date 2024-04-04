from ...utils import internal_error


class RToken:
    def __init__(self, text, _range):
        self.text = text
        self.range = _range

    def __repr__(self):
        return 'Token ( ' + str(self.text) + ' ' + str(self.range) + ' )'


class Register:
    def __init__(self):
        self.name = None
        self.type = None

        self.name_range = None
        self.type_range = None

        self.addresses = []
        self.address_ranges = []

        self.fields = []

        self.extra_infos = []

    def copy(self):
        nr = self.__class__()
        nr.name = self.name
        nr.type = self.type

        nr.name_range = self.name_range
        nr.type_range = self.type_range

        nr.addresses.extend(self.addresses)
        nr.address_ranges.extend(self.address_ranges)

        for fld in self.fields:
            nr.fields.append(fld.copy())

        for ei in self.extra_infos:
            nr.extra_infos.append(ei.copy())

        return nr

    def __contains__(self, k):
        for fld in self.fields:
            if fld.name == k:
                return True
        return False

    def __getitem__(self, k):
        if not isinstance(k, str): raise TypeError
        if k not in self: raise KeyError

        for fld in self.fields:
            if fld.name == k:
                return fld

        internal_error()


class Field:
    def __init__(self):
        self.name = ''
        self.bits = None
        self.type = None

        self.name_range = None
        self.bits_range = None
        self.type_range = None

        self.extra_infos = []

    def copy(self):
        nf = self.__class__()

        nf.name = self.name
        nf.bits = self.bits
        nf.type = self.type

        nf.name_range = self.name_range
        nf.bits_range = self.bits_range
        nf.type_range = self.type_range

        for ei in self.extra_infos:
            nf.extra_infos.append(ei.copy())

        return nf

    def is_valid_value(self, v):
        return 0 <= v and v < self.value_bound
    
    @property
    def value_bound(self):
        return 1 << (self.bits[0] + 1 - self.bits[1])


class ExtraInfo:
    def __init__(self, k, v, r):
        self.key = k
        self.value = v
        self.range = r

    def copy(self):
        return self.__class__(
            self.key,
            self.value,
            self.range
        )
