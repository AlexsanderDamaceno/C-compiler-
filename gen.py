import ast as Ast
from lex import tokens
from ast import Ast_Type
import sys



class Code_Gen():

  def __init__(self , prog):
       self.code           = ""
       self.prog           = prog
       self.labelnum       = 0
       self.reg_args       = ['rdi' , 'rsi' , 'rdx' , 'rcx' , 'r8' , 'r9' ]
       self.current_func   = None
  def stack_align(self , value ,  align):

      return (value + align-1)  & (-align)
  def append_cmd(self, cmd):
      self.code +=  cmd  + "\n"
      return
  def push(self , reg):
      self.append_cmd('  push %{}'.format(reg))
      return
  def pop(self , reg):
       self.append_cmd('  pop %{}'.format(reg))
       return
  def get_addr(self , node):

      if isinstance(node , Ast.Unary):
       if node.type == Ast_Type.DEREF:
        self.gen_expr(node.expr)
        return

      self.append_cmd("  lea {}(%rbp) , %rax".format(node.Decl.offset))
      return
  def gen_expr(self , ast):
     if isinstance(ast , Ast.Num):
         self.append_cmd("  mov ${} , %rax".format(ast.value))
         return
     if isinstance(ast , Ast.Identifier):

        self.get_addr(ast)
        self.append_cmd("  mov (%rax), %rax")
        return


     if isinstance(ast , Ast.Function_Call):

          for arg in ast.args:
              self.gen_expr(arg)
          if len(ast.args) > 0:
           for i in range(len(ast.args) , -1 , -1):
              self.pop(self.reg_args[i])

          self.append_cmd("  mov $0 , %rax")
          self.append_cmd("  call {}".format(ast.name))
          return


     if ast.type == Ast_Type.ADDR:

       self.get_addr(ast.expr)
       return

     if ast.type == Ast_Type.DEREF:
       self.gen_expr(ast.expr)
       self.append_cmd("  mov (%rax) , %rax")

       return


     if ast.type == Ast_Type.NEG:
         self.gen_expr(ast.expr)
         self.append_cmd('  neg %rax')
         return




     if isinstance(ast , Ast.Assign):

            self.get_addr(ast.left)
            self.push('  rax')
            self.gen_expr(ast.right)
            self.pop('  rdi')
            self.append_cmd('  mov %rax , (%rdi)')
            return



     self.gen_expr(ast.right)
     self.push('  rax')
     self.gen_expr(ast.left)
     self.pop('  rdi')


     if ast.type == Ast_Type.PLUS:

         self.append_cmd('  add %rdi , %rax')
         return
     elif  ast.type == Ast_Type.SUB:
         self.append_cmd('  sub %rdi , %rax')
         return
     elif  ast.type == Ast_Type.MUL:
         self.append_cmd('  imul %rdi , %rax')
         return
     elif  ast.type == Ast_Type.DIV:
         self.append_cmd('  cqo')
         self.append_cmd('  idiv %rdi')
         return
     elif ast.type == Ast_Type.LESS or ast.type == Ast_Type.GREATER:
         self.append_cmd('  cmp %rdi , %rax')
         self.append_cmd('  setl %al')
         self.append_cmd('  movzb %al , %rax')
         return
     elif ast.type == Ast_Type.GREATER_EQUAL or ast.type == Ast_Type.LESS_EQUAL:
         self.append_cmd('  cmp %rdi , %rax')
         self.append_cmd('  setle %al')
         self.append_cmd('  movzb %al , %rax')
         return
     elif ast.type == Ast_Type.EQUAL_EQUAL:
          self.append_cmd('  cmp %rdi , %rax')
          self.append_cmd('  sete %al')
          self.append_cmd('  movzb %al , %rax')
          return
     elif  ast.type == Ast_Type.NOT_EQUAL:
         self.append_cmd('  cmp %rdi , %rax')
         self.append_cmd('  setne %al')
         self.append_cmd('  movzb %al , %rax')
         return


     return
  def make_stmt(self , ast):



          if ast.type == Ast_Type.RETURN:

               self.gen_expr(ast.expr)
               self.append_cmd("  jmp .L.return.{}".format(self.current_func.func_name))
               return
          if ast.type == Ast_Type.EXPR_STMT:
              self.gen_expr(ast.expr)
              return

          if ast.type == Ast_Type.IF:

                    self.labelnum += 1
                    label_num = self.labelnum


                    self.gen_expr(ast.cond)
                    self.append_cmd("  cmp $0 , %rax")
                    self.append_cmd("  je .L.else{}".format(label_num))
                    self.make_stmt(ast.then)
                    self.append_cmd("  jmp .L.end{}".format(label_num))
                    self.append_cmd(".L.else{}:".format(label_num))
                    if ast.els != None:
                        self.make_stmt(ast.els)

                    self.append_cmd(".L.end{}:".format(label_num))
                    return

          if ast.type == Ast_Type.FOR:

                     self.labelnum += 1
                     label_num = self.labelnum
                     if ast.init != None:
                        self.make_stmt(ast.init)
                     self.append_cmd(".L.begin{}:".format(label_num))

                     if ast.cond != None:
                         self.gen_expr(ast.cond)
                         self.append_cmd("  cmp $0 , %rax")
                         self.append_cmd("  je .L.end{}".format(label_num))

                     self.make_stmt(ast.body)

                     if ast.inc != None:
                          self.gen_expr(ast.inc)
                     self.append_cmd("  jmp .L.begin{}".format(label_num))
                     self.append_cmd(".L.end{}:".format(label_num))
                     return



          if isinstance(ast , Ast.Compound_stmt):
            for stmt in ast.stmt_list:
              if stmt != None:
                self.make_stmt(stmt)
          return


  def determine_var_offset(self):

    for  function in self.prog:
      offset = 0
      for var in function.locals:
          offset += 8
          var.Decl.offset = -offset
      function.stack_size = self.stack_align(offset , 16)
      print(function.stack_size)
    return


  def  make_gen(self):
       stack_size =  self.determine_var_offset()

       for  function in self.prog:
         self.current_func  = function
         self.append_cmd('\n')
         self.append_cmd(".globl {}".format(function.func_name))
         self.append_cmd('\n')
         self.append_cmd("{}:".format(function.func_name))


         self.append_cmd("  push %rbp")
         self.append_cmd("  mov %rsp , %rbp".format(function.func_name))
         print(function.stack_size)
         self.append_cmd("sub ${} , %rsp".format(function.stack_size))

         self.make_stmt(function.body)

         self.append_cmd(".L.return.{}:".format(function.func_name))
         self.append_cmd("  mov %rbp , %rsp")
         self.append_cmd("  pop %rbp")
         self.append_cmd("  ret")

       return self.code
