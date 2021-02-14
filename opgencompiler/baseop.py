import numpy as np
from . import dtype

class ImplBuilder:

    def __init__(self, op, types_dict, name):
        self.op = op
        self.types_dict = types_dict
        self.name = name
        self.impl = None
        pass

    def native(self, name):
        return name

    def end(self, impl):
        self.impl = impl

# Create a constant during the test
# Will be resolved to the right type depending on the expected input type
class TestValConst:

    def __init__(self, data):
        self.data = data

    def get_val(self, str_type):
        dt = dtype.to_np_dtype(dtype.from_str(str_type))
        return np.array(self.data, dtype=dt)

class TestBuilder:

    def __init__(self, op, name, types_dict, impl):
        self.op = op
        self.name = name
        self.types_dict = types_dict
        self.impl = impl
        self.checks = []

        (args, rets) = self.op._decl().get_resolved_decl(self.types_dict)
        self.decl_args = args
        self.decl_rets = rets
        

    def add(self, inputs, exp):

        # Resolve input args
        inputs = [v.get_val(self.decl_args[i]) for (i, v) in enumerate(inputs)]

        # Resolve expected rets
        exp = [v.get_val(self.decl_rets[i]) for (i, v) in enumerate(exp)]

        if len(inputs) != len(self.decl_args):
            raise ValueError('Invaid test: incorrect number of arguments')
        if len(exp) != len(self.decl_rets):
            raise ValueError('Invalid test: incorrect number of results')
        
        self.checks.append((inputs, exp))

    def end(self):
        self.op._tests.append(self)

class TestsBuilderWrapper:

    def __init__(self, op, tests):
        self.op = op
        self.tests = tests

    def const(self, data):
        return TestValConst(data)

    def add(self, inputs, exp=None):
        for t in self.tests:
            t.add(inputs, exp)

    def end(self):
        for t in self.tests:
            t.end()

class BaseOp:
    def __init__(self):
        self.decl = None
        self.description = None

        self._decl_ready = False
        self._impls = {}
        self._tests = []
        


    def _decl(self):
        assert self.decl is not None

        if self._decl_ready is True:
            return self.decl

        self._decl_ready = True
        return self.decl

    def list_all_impls(self):
        return list(_impls.keys())

    def add_impl(self, types_dict, name):
        self._decl().check_assigns(types_dict)
        rt = ImplBuilder(self, types_dict, name)
        if name not in self._impls:
            self._impls[name] = []

        self._impls[name].append((types_dict, rt))
        return rt

    def add_test(self, name, types, impls):
        decl = self._decl()

        tests = []
        
        if types == '*':
            types = decl.gen_all_assigns()
        if impls == '*':
            impls = self.list_all_impls()

        for types_dict in types:
            for impl in impls:
                tests.append(self._add_test(name, types_dict, impl))

        return TestsBuilderWrapper(self, tests)

    def _add_test(self, name, types_dict, impl):
        decl = self._decl()
        ts_name = '{}.{}.{}'.format(name, decl.to_unique_name(types_dict), impl)
        return TestBuilder(self, ts_name, types_dict, impl)
