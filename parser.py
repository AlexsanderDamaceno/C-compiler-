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
      left  = sema.add_type(left)
      right = sema.add_type(right) 
      
      
      if sema.is_integer(left)  and sema.is_integer(right):
           print('')
           return  Ast.BinOp(left ,  Ast_Type.PLUS  , right)

      
      if sema.is_ptr(left)  and sema.is_ptr(right):
           print('invalid operands')
           sys.exit(-1)

      if   sema.is_ptr(right):
            tmp   = right
            right = left 
            left = tmp
      right =  Ast.BinOp(right , Ast_Type.MUL   , Ast.Num('8'))
      return    Ast.BinOp(left , Ast_Type.PLUS   , right)

    def process_sub(self , left , right):
     
    
      
      left  = sema.add_type(left)

      right = sema.add_type(right) 
      
      
      if sema.is_integer(left)  and sema.is_integer(right):
           return  Ast.BinOp(left ,  Ast_Type.SUB  , right)

      
   
      if sema.is_ptr(left) and sema.is_integer(right):
        right =  Ast.BinOp(right , Ast_Type.MUL   , Ast.Num('8'))
        add_type(right)
        return    Ast.BinOp(left , Ast_Type.SUB   , right)

      if sema.is_ptr(left) and sema.is_ptr(right):

        node =  Ast.BinOp(left , Ast_Type.SUB   , right)
        node.kind = sema.Int_Type
        return    Ast.BinOp(node , Ast_Type.DIV   , Ast.Num('8'))  

        



    def mul_div(self):
        left  = self.unary()
        Token =   self.peek()
        while Token.type == 'MUL' or  Token.type == 'DIV':
            self.Advance()
            ty = None
            if  Token.type == 'MUL':
                ty = Ast_Type.MUL
            else:
                ty = Ast_Type.DIV
            left = Ast.BinOp(left , ty  , self.unary())

            Token = self.peek()
        return left

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
                  
        return self.primary()


    def primary(self):

      Token = self.Advance()
      
      if  Token.type == 'LPAREN':
          ast = self.add_sub()

          Token = self.Advance()
          self.check(Token , 'RPAREN')
          return ast

      if Token.type  == 'NUMBER':
        return Ast.Num(Token.value)
      if Token.type  == 'NUMBER':
        return Ast.Num(Token.value)
      if Token.type  == 'ID':
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

    def declarator(self , base_ty):
      ty = base_ty 
      while self.peek().type == 'MUL':
        self.Advance()
        ty = sema.pointer_to(ty)

      

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
             Token.Advance()
             self.check(Token , 'COMMA')
             depth += 1 

         
          ty = self.declarator(base_ty)

          Token =  self.Advance() 
         
           
         
          self.check(Token , 'ID')

          var = Ast.Identifier(Token.value ,  Ast.Decl(Token.value , ty))
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
           
                       stmt_list.append(decl)
                 else:   
                       stmt_list.append(self.stmt())
           self.Advance()
           
           return Ast.Compound_stmt(Ast_Type.COMPOUND_STMT , stmt_list)






    def  print_ast(self, ast):
          if isinstance(ast , Ast.Num):
              print("number: ".format(ast.value))
              return
          print_ast(ast.left)
          print_ast(ast.right)
          print('+')
          return



    def make_ast(self):
      self.tokens = Tokenizer.make_token(self.source)
      
      
      token = self.Advance()
      self.check(token , 'LBRACE')

      #self.print_ast(self.add())
      return Ast.Function(self.compound_stmt() , self.locals)
