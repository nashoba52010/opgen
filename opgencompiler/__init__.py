
from .baseop import BaseOp
from .decl import Decl, DeclVarType
from . import dtype

_ops = []

def register_ops(ops):
    for Op in ops:
        _ops.append(Op())


def run(args):
    from .generator import Generator
    gen = Generator(_ops)
    gen.run()
