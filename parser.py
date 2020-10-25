import ast as Ast
from ast import Ast_Type
import lex as Tokenizer
from lex import tokens
import ply.lex as lex
import sys

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

        print(Token)
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
        left  = self.mul_div()
        Token =   self.peek()
        while Token.type == 'PLUS' or  Token.type == 'SUB':
            self.Advance()
            ty = None
            if  Token.type == 'PLUS':
                ty = Ast_Type.PLUS
            else:
                ty = Ast_Type.SUB

            left = Ast.BinOp(left ,  ty  , self.mul_div())
            Token = self.peek()

        return left

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
           if Identifier.Object.name == Token.value:

                return Ast.Identifier(Identifier.Object)


       var =  Ast.Identifier(Ast.Object(Token.value))
       self.locals.append(var)
       return var
      self.expected(Token , 'NUMBER or Identifier')
      return


    def expr(self):
        return  self.assign()
    def expr_stmt(self):

       if self.peek().type == 'COMMA':
           self.Advance()
           return None


       smt   =  Ast.Unary(Ast_Type.EXPR_STMT , self.expr())
       Token = self.Advance()
       self.check(Token , 'COMMA' )
       return smt




    def stmt(self):

       if self.peek().type == 'RETURN':
           self.Advance()
           node = Ast.Unary(Ast_Type.RETURN , self.expr())
           token = self.Advance()
           self.check(token , 'COMMA')
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
            if self.peek().type != 'COMMA':
                cond = self.expr()
            Token = self.Advance()
            self.check(Token , "COMMA")

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

    def compound_stmt(self):
           stmt_list  = []
           while self.peek().type != 'RBRACE':
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
