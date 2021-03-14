from .generatorcggrt import GeneratorCGGRT

# Starting point from writing code for a specific operation
class Generator:

    def __init__(self, ops, implem):
        self.ops = ops
        self.implem = implem
        self.cggrt_dir = '/home/obs/mytf/cggrt' # @[TODO] Find dir auto

    def run(self):
        gen = GeneratorCGGRT(self.cggrt_dir, self.implem)
        for op in self.ops:
            gen.cgen_op(op)
