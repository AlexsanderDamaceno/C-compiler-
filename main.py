import parser
import gen
import subprocess
import sema

f = open('teste.c' , 'r')
file_content = f.read()

parser    = parser.Parser(file_content)
ast       = parser.make_ast()


output_file = open('out.s' , 'w')



code_gen = gen.Code_Gen(ast)
code     = code_gen.make_gen()



code_gen = gen.Code_Gen(ast)
code     = code_gen.make_gen()



output_file.write(code)

#output_file.write('ret' + "\n")
output_file.close()
subprocess.call(['gcc' , '-static' ,  '-o' , 'outr' , 'out.s'])
