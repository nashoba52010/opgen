

class CWriter:

    def __init__(self, os):
        self.os = os

    def include_guard(self):
        self.os.write('#pragma once\n')

    def include(self, path, system=False):
        if system:
            self.os.write('#include <{}>\n'.format(path))
        else:
            self.os.write('#include "{}"\n'.format(path))

    def define(self, key, val):
        self.os.write('#define {} ({})\n'.format(key, val))

    def include_sys(self, path):
        self.include(path, system=True)

    def struct_def(self, name, fields):
        self.os.write('struct {} {{\n'.format(name))
        for f in fields:
            if isinstance(f, str):
                self.os.write('  {}\n'.format(f));
            else:
                self.os.write('  {} {};\n'.format(f[0], f[1]));
        self.os.write('};\n')


    def fun_def(self, name, args, ret_ty, is_static=False, is_inline=False, body=None):
        is_decl = body is not None
        if is_inline:
            is_static = True

        if is_static:
            self.os.write('static ')
        if is_inline:
            self.os.write('inline ')
        
        self.os.write('{} {}('.format(ret_ty, name))
        self.os.write(', '.join([
            '{} {}'.format(arg[0], arg[1]) for arg in args
            ]))

        self.os.write(')')

        if not is_decl:
            self.os.write(';\n')
            return

        
        self.os.write(' {\n')
        indent = 2

        #dump fun body
        for line in body:
            line = line.strip()
            if len(line) == 0:
                self.os.write('\n')
                continue

            self.os.write(' ' * indent)

            if line[-1] == '{':
                step += 2
            elif line[-1] == '}':
                step -= 2
            else:
                line += ';'
            self.os.write('{}\n'.format(line))

                
        self.os.write('}\n')
                      
        
        
        
