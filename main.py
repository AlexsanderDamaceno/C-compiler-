import parser
import gen
import subprocess

f = open('teste.c' , 'r')
file_content = f.read()

parser = parser.Parser(file_content)
ast    = parser.make_ast()

output_file = open('out.s' , 'w')



code = '.globl main' + "\n"
code += 'main:' + "\n"
code += 'push %rbp' + "\n"
code += 'mov %rsp , %rbp' + "\n"

code_gen = gen.Code_Gen(ast)
code     += code_gen.make_gen()
code += ".L.return:"  + "\n"
code += 'mov %rbp , %rsp' + "\n"
code += 'pop %rbp' + "\n"
code += 'ret' + "\n"
print(code)
output_file.write(code)

#output_file.write('ret' + "\n")
output_file.close()
subprocess.call(['gcc' , '-static' ,  '-o' , 'outr' , 'out.s'])
