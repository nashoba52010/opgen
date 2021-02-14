import numpy as np

F32 = 1
F64 = 2
UNK = -1


def from_str(s):
    if s == 'f32':
        return F32
    elif s == 'f64':
        return F64
    else:
        raise ValueError('Unknown type `{}'.format(s))

def to_np_dtype(t):
    if t == F32:
        return np.float32
    elif t == F64:
        return np.float64
