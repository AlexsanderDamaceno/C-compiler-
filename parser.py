import ast as Ast
from ast import Ast_Type
import lex as Tokenizer
from lex import tokens
import ply.lex as lex
import sema
import sys
from sema import Int_Type
offset = 0

class Parser():

    def __init__(self ,  source):
        self.offset = 0
        self.source = source
        self.tokens = None
        self.locals = []


    def Advance(self):
        if  self.offset >= len(self.tokens):
            self.to += 1
        actual      = self.tokens[self.offset]
        self.offset += 1
        return actual
    def peek(self):
        if  self.offset >= len(self.tokens):
                return -1
        return self.tokens[self.offset]

    def check(self , token ,  expected_type):
       if token.type != expected_type:
         print('Error expected {} but got {} at line {}'.format(expected_type , token.type , token.lineno ))
         sys.exit(-1)
       return
    def expected(self , token , expected_type):
         if token.type == 'eof':
             token.lineno -= 1
         print('Error expected {} but got {} at line {}'.format(expected_type , token.type , token.lineno ))
         sys.exit(-1)

    def assign(self):
        node  = self.equality()
        Token =   self.peek()


        if Token.type == 'ASSIGN':

            self.Advance()
            node  = Ast.Assign(node , Ast_Type.ASSIGN  , self.assign())


        return node

    def equality(self):
            left = self.relational()

            while True:
                if self.peek().type == 'EQUAL_EQUAL':
                    self.Advance()
                    left =  Ast.BinOp(left , Ast_Type.EQUAL_EQUAL   , self.relational())
                    continue
                if self.peek().type == 'NOT_EQUAL':
                    self.Advance()
                    left =   Ast.BinOp(left , Ast_Type.NOT_EQUAL   , self.relational())
                    continue
                break
            return left

    def relational(self):
        left = self.add_sub()

        while True:
            if self.peek().type == 'LESS':
                self.Advance()
                left =  Ast.BinOp(left , Ast_Type.LESS   , self.add_sub())
                continue
            if self.peek().type == 'LESS_EQUAL':
                self.Advance()
                left =   Ast.BinOp(left , Ast_Type.LESS_EQUAL   , self.add_sub())
                continue
            if self.peek().type == 'GREATER':
                self.Advance()
                left =  Ast.BinOp(left , Ast_Type.GREATER , self.add_sub())
                continue
            if self.peek().type == 'GREATER_EQUAL':
                self.Advance()
                left =   Ast.BinOp(left , Ast_Type.GREATER_EQUAL   , self.add_sub())
                continue
            break
        return left

    def add_sub(self):
        node  = self.mul_div()
        Token =   self.peek()

        while Token.type == 'PLUS' or  Token.type == 'SUB':

           if  Token.type == 'PLUS':

            self.Advance()
            right  = self.mul_div()
            node   = self.process_add(node , right)
           else:
            self.Advance()
            right  = self.mul_div()
            node   =  self.process_sub(node , right)
           Token = self.peek()


        return node


    def process_add(self , left  , right):
      
      if isinstance(left , Ast.Num) and isinstance(right  , Ast.Num):
          return Ast.Num(str(int(left.value) + int(right.value)))

      left  = sema.add_type(left)

      right = sema.add_type(right)

     
      
      if sema.is_integer(left)  and sema.is_integer(right):
           
           return  Ast.BinOp(left ,  Ast_Type.PLUS  , right)

     
      if sema.is_ptr(left)  and sema.is_ptr(right):
           print('invalid operands')
           sys.exit(-1)

      if   sema.is_ptr(right):
            tmp   = right
            right = left
            left = tmp
      

      right =  Ast.BinOp(right , Ast_Type.MUL   , Ast.Num(left.kind.base.size))
      
      return    Ast.BinOp(left , Ast_Type.PLUS   , right)

    def process_sub(self , left , right):

      if isinstance(left , Ast.Num) and isinstance(right  , Ast.Num):
          return Ast.Num(str(int(left.value) - int(right.value)))

      left  = sema.add_type(left)

      right = sema.add_type(right)


      if sema.is_integer(left)  and sema.is_integer(right):
           return  Ast.BinOp(left ,  Ast_Type.SUB  , right)



      if sema.is_ptr(left) and sema.is_integer(right):
        right =  Ast.BinOp(right , Ast_Type.MUL   , Ast.Num(left.Decl.base.size))
        add_type(right)
        return    Ast.BinOp(left , Ast_Type.SUB   , right)

      if sema.is_ptr(left) and sema.is_ptr(right):

        node =  Ast.BinOp(left , Ast_Type.SUB   , right)
        add_type(node)
        return    Ast.BinOp(node , Ast_Type.DIV   , Ast.Num(left.Decl.base.size))





    def mul_div(self):
        node  = self.unary()
        Token =   self.peek()
        while Token.type == 'MUL' or  Token.type == 'DIV':

            self.Advance()
            ty = None
            if  Token.type == 'MUL':
                ty = Ast_Type.MUL
            else:
                ty = Ast_Type.DIV
            right = self.unary()

            if isinstance(node , Ast.Num) and isinstance(right  , Ast.Num):
              if ty == Ast_Type.MUL:
                  node =  Ast.Num(str(int(node.value) * int(right.value)))
              else:
                  node  =  Ast.Num(str(int(node.value) / int(right.value)))
              Token = self.peek()
              continue



            node = Ast.BinOp(node , ty  ,  right )

            Token = self.peek()
        return node

    def unary(self):
        if   self.peek().type == 'PLUS':
            self.Advance()
            return self.unary()
        if   self.peek().type == 'SUB':


            self.Advance()
            return Ast.Unary(Ast_Type.NEG , self.unary())

        if   self.peek().type == 'MUL':
            self.Advance()
            return Ast.Unary(Ast_Type.DEREF , self.unary())
        if   self.peek().type == 'ADDR_BIT':
            self.Advance()

            return Ast.Unary(Ast_Type.ADDR , self.unary())

        return self.suffix()


    def suffix(self):
        node = self.primary()
        
        while self.peek().type == 'LBRACKET':
          self.Advance()
          index = self.expr()
          self.check(self.peek() , 'RBRACKET')
          node = Ast.Unary(Ast_Type.DEREF  , self.process_add(node , index))
          self.Advance()

        return node


    def funcall(self , func_name):
        args = []
        depth = 0
        while self.peek().type != 'RPAREN':
            if depth > 0:
                self.check(self.Advance() , 'COMMA')

            args.append(self.assign())
            depth += 1

        self.Advance()
        node = Ast.Function_Call(func_name , args)
        return node

    def primary(self):

      Token = self.Advance()

      if  Token.type == 'LPAREN':
          ast = self.add_sub()

          Token = self.Advance()
          self.check(Token , 'RPAREN')
          return ast

      if Token.type  == 'NUMBER':
        return Ast.Num(Token.value)

     
      if Token.type == 'SIZEOF':
          
          node = self.unary()
          sema.add_type(node)
          return Ast.Num(node.kind.size)    


      if Token.type  == 'ID':

       if self.peek().type == 'LPAREN':
          self.Advance()
          return self.funcall(Token.value)



       for Identifier in self.locals:
           if Identifier.Decl.name == Token.value:
                return Ast.Identifier(Token.value , Identifier.Decl)
       print("Variable {}  undeclared  at line {} ".format(Token.value , Token.lineno))
       sys.exit(-1)

      self.expected(Token , 'NUMBER or Identifier')
      return


    def expr(self):
        return  self.assign()
    def expr_stmt(self):

       if self.peek().type == 'SEMICOLON':
           self.Advance()
           return None


       smt   =  Ast.Unary(Ast_Type.EXPR_STMT , self.expr())
       Token = self.Advance()
       self.check(Token , 'SEMICOLON' )
       return smt




    def stmt(self):

       if self.peek().type == 'RETURN':
           self.Advance()
           node = Ast.Unary(Ast_Type.RETURN , self.expr())
           token = self.Advance()
           self.check(token , 'SEMICOLON')
           return node
       elif  self.peek().type == 'LBRACE':
           self.Advance()
           return self.compound_stmt()
       elif self.peek().type == 'IF':
           self.Advance()
           Token =  self.Advance()
           self.check(Token , 'LPAREN')

           cond = self.expr()

           Token =  self.Advance()
           self.check(Token , 'RPAREN')

           then = self.stmt()
           els  = None
           if self.peek().type == 'ELSE':
               self.Advance()
               els = self.stmt()
           return  Ast.If(Ast_Type.IF , cond , then , els)


       elif self.peek().type == 'FOR':
            self.Advance()

            Token = self.Advance()
            self.check(Token , "LPAREN")

            init = self.expr_stmt()

            cond = None
            if self.peek().type != 'SEMICOLON':
                cond = self.expr()
            Token = self.Advance()
            self.check(Token , "SEMICOLON")

            inc = None
            if self.peek().type != 'RPAREN':
                inc = self.expr()
            Token = self.Advance()

            self.check(Token , "RPAREN")

            body  = self.stmt()
            return Ast.For(Ast_Type.FOR  , init , cond , inc , body)

        # change while to for
       elif self.peek().type == 'WHILE':

            self.Advance()

            Token = self.Advance()
            self.check(Token , "LPAREN")

            cond = None
            cond = self.expr()

            Token = self.Advance()

            self.check(Token , "RPAREN")

            body  = self.stmt()
            return Ast.For(Ast_Type.FOR  , None , cond, None , body)










       return self.expr_stmt()

    #def suffix(self):
    #    if self.peek().type == 'LPAREN':


    def get_number(self):
      self.check(self.peek() , 'NUMBER')
      return self.Advance().value

    def type_suffix(self , ty):
        
       
           
          

        if self.peek().type == 'LBRACKET':
           self.Advance()
           size  = self.get_number()
           self.check(self.peek() , 'RBRACKET')
           self.Advance()
           ty  = self.type_suffix(ty)
           return sema.array_of(ty , int(size)) 
          
        return ty   




    def declarator(self , base_ty):
      ty = base_ty
      while self.peek().type == 'MUL':
        self.Advance()
        ty = sema.pointer_to(ty)

      self.check(self.peek() , 'ID')
      
      name = self.Advance()
     

      
      ty  = self.type_suffix(ty)
     
      ty.name =  name
      return ty



      








    def declaration_specs(self):
      Token = self.Advance()
      self.check(Token ,  'INT')
      return sema.Int_Type

    def declaration(self):
      base_ty = self.declaration_specs()

      depth = 0

      var_decl_stmt = []

      while not self.peek().type == 'SEMICOLON':


          if depth > 0:
             Token = Token.Advance()
             self.check(Token , 'COMMA')
             depth += 1
         

          ty = self.declarator(base_ty)

          var = Ast.Identifier(ty.name.value ,  Ast.Decl(ty.name.value, ty))
          self.locals.append(var)


          if self.peek().type != 'ASSIGN':
             continue
          self.Advance()

          left  =  var
          right =  self.assign()


          var_decl_stmt.append(Ast.Unary(Ast_Type.EXPR_STMT , Ast.Assign(left , Ast_Type.ASSIGN  , right)))





      self.Advance()

      return var_decl_stmt








    def compound_stmt(self):
           stmt_list  = []
           while self.peek().type != 'RBRACE':
                 if self.peek().type == 'INT':
                    decls = self.declaration()
                    for decl in decls:

                       decl = sema.add_type(decl) 

                       

                       stmt_list.append(decl)
                 else:

                       stmt = sema.add_type(self.stmt())
                      
                       stmt_list.append(stmt)
           self.Advance()

           return Ast.Compound_stmt(Ast_Type.COMPOUND_STMT , stmt_list)


    def params(self):
        params_list = []
        depth = 0
        while self.peek().type != 'RPAREN':
            if depth > 0:
                 self.check(self.Advance() , 'COMMA')
            depth += 1     

            base_ty = self.declaration_specs()
            ty      = self.declarator(base_ty)
            
            
            node = Ast.Identifier(ty.name.value ,  Ast.Decl(ty.name.value , ty))
            params_list.append(node)
            self.locals.append(node)
        self.check(self.Advance() , 'RPAREN')
        return params_list



    def function(self):

       ty = self.declaration_specs()
       ty = self.declarator(ty)
       f_name = ty.name.value
      
       
       self.check(self.peek() , 'LPAREN')
       self.Advance()
       params = self.params()
       
       self.check(self.Advance() , 'LBRACE')
       body = self.compound_stmt()
       locals = self.locals
       
       return Ast.Function(f_name , params,  ty , body , locals)







    def make_ast(self):
      self.tokens = Tokenizer.make_token(self.source)
      function_list = []
      while self.peek().type != 'eof':
          function_list.append(self.function())
          self.locals = []
      return function_list
