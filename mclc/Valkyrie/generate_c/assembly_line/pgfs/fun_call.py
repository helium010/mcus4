def gen(gc, fc):

    from . import exp
    return "%s %s(%s)" % (
        "/* call function %s in %s */" % (
            fc.ref.last.object.id.text,
            fc.ref.last.object.id.range.file_dot_ref,
        ),
        gc.cst[fc.ref.last.object],
        ', '.join(
            [exp.gen(gc, pt) for pt in fc.params]
        )
    )
