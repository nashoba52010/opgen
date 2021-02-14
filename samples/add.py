

class Add(Opdef):

    def __init__(self):

        # raw operation declaration
        self.decl = OpDecl('add', [VarType('T'), VarType('T')], [VarType('T')],
                           {'T': ['f32', 'f64']})

        # string-like operation declaration
        self.decl = 'add (x:T, y:T) -> (res:T) <T:f32,f64>'

        # long description
        self.description = 'Element-whise addition'

        # create op implementation vanilla for f32
        rt = self.add_impl({'T': 'f32'}, 'van')
        rt.end(rt.native('mykernels_op_add_van_f32'))

        # create test1
        ts = self.add_test('basic_add', ['f32', 'f64'], '*')
        ts.add(inputs=[ts.const([3., 6., 8.]), ts.const([9., -1., 7.])],
               exp=[ts.const([12., 5, 15.])])
        ts.add(seed=187, inputs=[ts.randn([4, 6]), ts.randn([4, 6])],
               ref_fn=ref_add)
        ts.end()

        # create static input requirments
        (B, ins) = self.add_requirements('x and y must be of same shape')
        B.end(ins.x.shape == ins.y.shape)

        # create static input requirements
        self.extend([SameShapeOperands()])

        #define static output shape
        (B, ins) = self.add_outputs_def()
        B.end([ins.x.shape])

        # define output shape
        self.extend([OutputShapeSameAsInput()])

        # TODO: support for later
        # With this, the operation can return any shape type depending on the input
        # the real shape is only known when all the inputs are executed
        # all static requirements and output are only called when operation is ready to be executeed
        # could use special version add_dyn_requirements, add_dyn_output_defs
        # to be able to add some checks / return static ops for non-static ops
        # self.dyn_output_shape = True
        

    # Create static input requirments
    @kl_reqs('Both operands must have the same shape')
    def check_inputs(self, B, ins):
        return ins.x.shape == ins.y.shape

    # define static output shape
    @kl_outputs()
    def get_outputs(self, B, ins):
        return [ins.x.shape]
            
    
    # operation to get outputs tensor types / shapes
    def results(self):
        #TODO
        pass

    # create op implementation vanilla for f32
    @kl_impl({'T': 'f32'}, 'van'):
    @kl_impl('T=f32', 'van'):
    @kl_impl('f32', 'van'): #no need to specify type name when only one is available
    def impl_f32_van(self, rt):
        return rt.native('mykernels_op_add_van_f32')

    # create op implementation vanilla for f64
    @kl_impl('f64', 'van'):
    def impl_f64_van(self, rt):
        return rt.native('mykernels_op_add_van_f64')


    @kl_test('basic_add', ['f32', 'f64'], '*')
    def test1(self, ts):
        ts.add(inputs=[ts.const([3., 6., 8.]), ts.const([9., -1., 7.])],
               exp=[ts.const([12., 5, 15.])])
        ts.add(seed=187, inputs=[ts.randn([4, 6]), ts.randn([4, 6])],
               ref_fn=ref_add)


def ref_add(args):
    return [args[0] + args[1]]

                                 
