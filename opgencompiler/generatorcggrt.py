import os

from .cwriter import CWriter

def dt_to_cggrt_dt(dt):
    if dt == 'f32':
        return 'CGGRT_DT_F32'
    elif dt == 'f64':
        return 'CGGRT_DT_F64'
    else:
        assert 0

class GeneratorCGGRT:

    def __init__(self, proj_dir):
        self.proj_dir = proj_dir
        self.gen_src_dir = os.path.join(self.proj_dir, 'src/gen')
        self.gen_include_dir = os.path.join(self.proj_dir, 'include/cggrt/gen')

    def cgen_op(self, op):
        # gen all implementations
        for entry in op._impls.values():
            for impl in entry:
                self.cgen_impl(op, impl[1])


    def cgen_impl(self, op, builder):
        decl = op._decl()
        decl_args, decl_rets = decl.get_resolved_decl(builder.types_dict)
        decl_tys_name = decl.to_unique_name(builder.types_dict)
        optyname = 'cggrt_Node{}{}{}'.format(
            decl.name.title(),
            decl_tys_name.title(),
            builder.name.title())
        optymac = 'cggrt_node_op_{}_{}_{}'.format(
            decl.name, decl_tys_name, builder.name).upper()
        fname = 'node-op-{}-{}-{}'.format(
            decl.name,
            decl_tys_name.replace('_', '-'),
            builder.name)

        # Open source files
        hfile_path = os.path.join(self.gen_include_dir, '{}.h'.format(fname))
        cfile_path = os.path.join(self.gen_src_dir, '{}.c'.format(fname))
        hfile = CWriter(open(hfile_path, 'w'))
        cfile = CWriter(open(cfile_path, 'w'))
        for p in [cfile_path, hfile_path]:
            print('Writing {}...'.format(p))



        ### Op Header File ####

        # Prelude for header file
        hfile.include_guard()
        hfile.include("../fwd.h")
        hfile.include("../node.h")
        hfile.include("../shape.h") # @[TODO] only needed depending on attrs
        hfile.include("../types.h")

        # @[TODO] Create attrs class

        # define op struct
        hfile.struct_def('S_' + optyname, [
            'CGGRT_NODE_HEADERS',
            # @[TODO] Add attr class,
            ] +
        [('cggrt_Node*', name) for name in decl.args_names])

        # declare builder function
        build_fname = 'cggrt_Graph_op_{}_{}_{}'.format(decl.name, decl_tys_name, builder.name)
        build_args = [('cggrt_Graph*', 'g')] + [
                # @[TODO] Add attr class
            ] + [
                ('cggrt_Node*', name) for name in decl.args_names
            ]
        hfile.fun_def(build_fname, build_args, optyname + '*')

        # declare op fdyn functions
        hfile.fun_def(optyname + '_fdyn_exec', [('cggrt_Node*', 'node')], 'void')



        
        ### Op Src File ###

        # Prelude for src file
        cfile.include_sys("cggrt/graph.h")
        cfile.include_sys("cggrt/tensor.h")
        cfile.include_sys('cggrt/{}.h'.format(fname))

        # Add kernel declaration
        kernel_name = builder.impl
        cfile.fun_def(kernel_name, [
            ('cggrt_Tensor*', 'i_' + name) for name in decl.args_names
        ] + [
            ('cggrt_Tensor*', 'o_' + name) for name in decl.ret_names
        ] + [
            # @[TODO] Add attr class
        ], 'void')

        # Add builder definition
        cfile.fun_def(build_fname, build_args, optyname + '*', body = [
            # @[TODO] input checks

            '{} *node = ({}*) cggrt_Node_new(sizeof({}))'.format(optyname, optyname, optyname),
            'node->op = {}'.format(optymac),
            'node->state = CGGRT_NODE_ST_INVALID',
            'node->preds_count = {}'.format(len(decl.args)),

            # @[TODO] set attrs
            
            'node->result = cggrt_Tensor_new_1d(4096, {})'.format(
                dt_to_cggrt_dt(decl_rets[0])), # @[TODO] Use real shape

            'cggrt_Graph_finish_add(g, (cggrt_Node*)node)',
            'return node'
        ])

        # Add fdyn exec definition
        cfile.fun_def(optyname + '_fdyn_exec', [('cggrt_Node*', 'node')], 'void', body=[
            '{}* n = ({}*) node'.format(optyname, optyname),

            # function call to kernel function
            '{}({})'.format(kernel_name, ', '.join([
                '&node->' + name for name in decl.args_names
            ] + [
                '&node->' + name for name in decl.ret_names
            ] + [
                # @[TODO] Add attr param
            ])),

            
        ])

        #[TODO] Add to fdyn table

        #[TODO] Add include c to ops-all.c

        #[TODO] Add include h to ops-all.h

        #[TODO] Add typedef for struct node op

        #[TODO] Add define for op uid

        
