from .utils import assert_type, error


class Range:
    '''
    Contructors :
    ---------
        Range(fdr, sln, scol, eln, ecol)

        Range(fdr, ln, scol, ecol)

        Range(fdr, ln, col)

        Range(rng1, rng2)

    Descriptions :
    ---------
    An instance of Range is immutable, whose 
    properties cannot be changed after construction.

    A range consists of a file_dor_ref and four numbers, 
    all of the numbers are zero-based

    '''

    def __init__(self, file_dot_ref, *pos_args):

        def _assert_list_type(l, t):
            for i in l:
                assert_type(i, t)

        if len(pos_args) in range(2, 5):
            assert_type(file_dot_ref, str)
            self.file_dot_ref = file_dot_ref
            if len(pos_args) == 4:
                _assert_list_type(pos_args, int)
                self.sln = pos_args[0]
                self.scol = pos_args[1]
                self.eln = pos_args[2]
                self.ecol = pos_args[3]

            elif len(pos_args) == 3:
                _assert_list_type(pos_args, int)
                self.sln = pos_args[0]
                self.scol = pos_args[1]
                self.eln = pos_args[0]
                self.ecol = pos_args[2]

            elif len(pos_args) == 2:

                _assert_list_type(pos_args, int)
                self.sln = pos_args[0]
                self.scol = pos_args[1]
                self.eln = pos_args[0]
                self.ecol = pos_args[1]

        elif len(pos_args) == 1:
            ra = file_dot_ref
            rb = pos_args[0]

            assert_type(ra, Range)
            assert_type(rb, Range)
            if ra.file_dot_ref != rb.file_dot_ref:
                error('Ranges in different files cannot be concatenated.')

            self.file_dot_ref = ra.file_dot_ref

            if ra.sln < rb.sln:
                self.sln = ra.sln
                self.scol = ra.scol
            elif ra.sln == rb.sln:
                self.sln = ra.sln
                self.scol = min(ra.scol, rb.scol)
            else:
                self.sln = ra.sln
                self.scol = rb.scol

            if ra.eln > rb.eln:
                self.eln = ra.eln
                self.ecol = ra.ecol
            elif ra.eln == rb.eln:
                self.eln = ra.eln
                self.ecol = max(ra.ecol, rb.ecol)
            else:
                self.eln = rb.eln
                self.ecol = rb.ecol

        else:
            error('Not a valid constructor of Range')

    def dict(self):
        return {
            'fdr': self.file_dot_ref,
            'sln': self.sln,
            'scol': self.scol,
            'eln': self.eln,
            'ecol': self.ecol
        }

    def __repr__(self):
        return 'Rng(%s %d,%d - %d,%d)' % (self.file_dot_ref, self.sln, self.scol, self.eln, self.ecol)

    def __setattr__(self, attr, value):
        if attr not in ('file_dot_ref', 'sln', 'scol', 'eln', 'ecol'):
            error("Properties of Range other than 'file_dot_ref', 'sln', 'scol', 'eln' and 'ecol' are not allowed ")

        if attr in self.__dict__:
            error('Range is immutable.')
        super().__setattr__(attr, value)

    def __contains__(self, args):
        if len(args) not in [2, 3]: raise TypeError

        if len(args) == 3:
            if args[0] != self.file_dot_ref: return False
            ln = args[1]
            col = args[2]
        else:
            ln = args[0]
            col = args[1]

        # before fisrt line or after last line
        if ln < self.sln or ln > self.eln:
            return False
        # before first column of first line
        if ln == self.sln:
            if col < self.scol:
                return False
        # after last column of last line
        if ln == self.eln:
            if col >= self.ecol:
                return False
        return True


class Diagnostic:

    def __init__(self, _range: Range, msg: str, severity='error', source=''):
        assert_type(_range, Range)
        assert_type(msg, str)

        self.range = _range
        self.msg = msg
        self.severity = severity
        self.source = source

    def __repr__(self):
        return 'Diag( ' + str(self.range) + ', ' + self.msg + ' )'

    def copy(self):
        return self.__class__(
            self.range,
            self.msg,
            self.severity
        )

    def dict(self):
        return {
            'range': self.range.dict(),
            'msg': self.msg,
            'severity': self.severity,
            'source': self.source
        }


class Highlight:

    def __init__(self, _range: Range, _type: str):
        assert_type(_range, Range)
        assert_type(_type, str)

        self.range = _range
        self.type = _type

    def __repr__(self):
        return 'Hlt( ' + str(self.range) + ', ' + self.type + ' )'

    def copy(self):
        return self.__class__(
            self.range,
            self.type,
        )

    def dict(self):
        return {
            'range': self.range.dict(),
            'type': self.type,
        }
