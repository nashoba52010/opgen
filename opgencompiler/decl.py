from . import dtype

# @[TODO] Add parser



class DeclVarType:

    def __init__(self, name):
        self.name = name
    

class Decl:

    def __init__(self, name, args, ret, vars_dict):
        self.name = name
        self.args_names, self.args = zip(*args)
        self.ret_names, self.ret =zip(*ret)
        self.vars_dict = vars_dict

        #build unique vars list
        self.vars_list = []
        for arg in (self.args + self.ret):
            if isinstance(arg, DeclVarType) and arg.name not in self.vars_list:
                self.vars_list.append(arg.name)

        # check declaration of variable types                
        for v in self.vars_list:
            self.get_var_choices(v)
        
        for (key, val) in vars_dict.items():
            if key not in self.vars_list:
                raise ValueError('Decl for `{}` has no variable type `{}`'.format(self.name, key))

            # check if all types exist
            for t in val:
                dtype.from_str(t)


    def get_var_choices(self, name):
        if name not in self.vars_dict:
            raise ValueError('Decl for `{}` has no variable type `{}`'.format(self.name,
                                                                              name))
        return self.vars_dict[name]
        

    # check if it's legal to use a specific type for a vartype
    def check_var_assign(self, key, val):
        types = self.get_var_choices(key)
        if val not in types:
            raise ValueError('Decl for `{}` doesn\'t allow type {} for {}. Not in '.format(
                self.name, val, key, types))

    # check if all assigments are complete, and none is missing
    def check_assigns(self, types_dict):
        for key in self.vars_dict:
            if key not in types_dict:
                raise ValueError('Decl `{}`: missing assignment for var {}'.format(
                    self.name, key))
        for key, val in types_dict.items():
            self.check_var_assign(key, val)
        

    # turn an assignment into a unique list of types
    def to_unique_name(self, types_dict):
        self.check_assigns(types_dict)
        return '_'.join([types_dict[v] for v in self.vars_list])

    # gen the list of all possible assigments
    def gen_all_assigns(self):
        res = []
        self._gen_all_assigns_rec(res, dict(), self.vars_list, 0)
        return res


    def _gen_all_assigns_rec(res, current, vtypes, vtypes_idx):
        if vtypes_idx == len(vtypes):
            res.append(current)
            return

        v = vtypes[vtypes_idx]
        for val in self.vars_dict[v]:
            other = dict(current)
            other[v] = val
            self._gen_all_assigns_rec(res, other, vtypes, vtypes_idx + 1)
        
        

    # return ([arg0, arg1, ...], [res0, res1, ...]) types list
    # resolves from assignments list
    def get_resolved_decl(self, types_dict):
        self.check_assigns(types_dict)

        full = []

        for v in (self.args + self.ret):
            if isinstance(v, DeclVarType):
                full.append(types_dict[v.name])

        return (full[:len(self.args)], full[len(self.args):])
        
        
    
