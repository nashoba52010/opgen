
from .baseop import BaseOp
from .decl import Decl, DeclVarType
from . import dtype

_ops = []

def register_ops(ops):
    for Op in ops:
        _ops.append(Op())


def parse_args(infos, args):
    res = {k : infos[k] for k in infos.keys()}
    for arg in args:
        if arg.startswith('--') and '=' in arg:
            key, val = arg[2:].split('=')
            if key in infos:
                res[key] = val

    return res
            
    

def run(args):
    implem = None

    args = parse_args({
        'implem': None,
    }, args)

    implem = args['implem']
    if implem is None:
        print('Missing implem argument')
    
    from .generator import Generator
    gen = Generator(_ops, implem)
    gen.run()
