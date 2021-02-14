import sys

import ops
import opgencompiler as ogc

if __name__ == '__main__':
    ogc.register_ops([
        ops.OpAdd
    ])
    ogc.run(sys.argv)
