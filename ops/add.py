import opgencompiler as ogc

class OpAdd(ogc.BaseOp):

    def __init__(self):
        super().__init__()

        self.decl = ogc.Decl('add', [('x', ogc.DeclVarType('T')),
                                     ('y', ogc.DeclVarType('T'))],
                             [('res', ogc.DeclVarType('T'))],
                             {'T': ['f32', 'f64']})
        self.description = 'Element-whise addition'

        # create op implementation vanilla for f32
        rt = self.add_impl({'T': 'f32'}, 'van')
        rt.end(rt.native('mykernels_op_add_van_f32'))

        # create op implementation vanilla for f64
        rt = self.add_impl({'T': 'f64'}, 'van')
        rt.end(rt.native('mykernels_op_add_van_f64'))

        # create test1
        ts = self.add_test('basic_add', [{'T': 'f32'}, {'T': 'f64'}], ['van'])
        ts.add(inputs=[ts.const([3., 6., 8.]), ts.const([9., -1., 7.])],
               exp=[ts.const([12., 5, 15.])])
        ts.end()
        
