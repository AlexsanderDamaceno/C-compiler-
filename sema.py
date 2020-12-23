import ast  as Ast
from   ast  import Ast_Type
from   ast  import Ast_TypeKind
import sys
Int_Type  = Ast.Type(Ast_TypeKind.TY_INT , None , 8)

def is_integer(ast):

  if isinstance(ast , Ast.Function_Call):
         if ast.ty == Int_Type:
             return True
         else:
             return False
  
  if ast.kind.type == Ast_TypeKind.TY_INT:
      return True
  else:
      return False

def is_ptr(ast):

  if ast.kind.type == Ast_TypeKind.TY_POINTER:
      return True
  else:
      return False


def pointer_to(base):
  return Ast.Type(Ast_TypeKind.TY_POINTER , base , 8)

def array_of(base_ty , len):
  return Ast.Type(Ast_TypeKind.TY_ARRAY , base_ty ,  base_ty.size * len)



def add_type(ast):
           global Int_Type

           if ast == None:
              return

           

           if isinstance(ast , Ast.For):
               if ast.init:
                    ast.init =  add_type(ast.init)
               if ast.cond:
                    ast.cond =  add_type(ast.cond)
               if ast.inc:
                   ast.inc = add_type(ast.inc)
               if ast.body:
                   ast.boy = add_type(ast.body)
               return ast

           if isinstance(ast , Ast.If):
               ast.cond =  add_type(ast.cond)
               ast.then =  add_type(ast.then)
               if ast.els:
                   ast.els = add_type(ast.els)
               return ast



           if isinstance(ast , Ast.Function_Call):
               ast.ty = Int_Type
               return ast

           if isinstance(ast , Ast.Num):
              ast.kind = Int_Type
              return ast
           if isinstance(ast , Ast.Identifier):

              ast.kind  = ast.Decl.ty
              return ast
           
           

           if isinstance(ast , Ast.BinOp):
             ast.left =  add_type(ast.left)
             ast.right = add_type(ast.right)


             if ast.type == Ast_Type.LESS   or   ast.type == Ast_Type.LESS_EQUAL:
              ast.kind =  Int_Type
              return ast
             if ast.type == Ast_Type.GREATER or   ast.type == Ast_Type.GREATER_EQUAL:
              ast.kind =  Int_Type
              return
             if ast.type == Ast_Type.PLUS  or ast.type == Ast_Type.SUB:
               ast.kind = ast.left.kind
               return ast
             if ast.type == Ast_Type.MUL  or ast.type == Ast_Type.DIV:
               ast.kind = ast.left.kind
               return ast

             
           if ast.type == Ast_Type.ASSIGN:
                
                 ast.left  =  add_type(ast.left)
                 ast.right =  add_type(ast.right)
                 if ast.left.kind.type == Ast.Ast_TypeKind.TY_ARRAY:
                      print('error not  lvalue')
                      sys.exit(-1)

                 ast.kind = ast.left.kind

                 return ast

                

           if isinstance(ast , Ast.Unary):
              
              ast.expr = add_type(ast.expr)
  
              
              if ast.type == Ast_Type.ND_MEMBER:

                ast.kind  = ast.member.type

              

              if ast.type == Ast_Type.NEG:

                 ast.kind = ast.left.kind

              if ast.type == Ast_Type.ADDR:
                if ast.expr.Decl.ty.type == Ast.Ast_TypeKind.TY_ARRAY:
                 ast.kind =   pointer_to(ast.expr.Decl.kind.base)    
                else:
                 ast.kind =   pointer_to(ast.expr.kind)
                 
                 

              if ast.type == Ast_Type.DEREF:
                
                if  ast.expr.kind.base == None:
                    print('invalid deref')
                    sys.exit(-1)

                else:

                 ast.kind =   ast.expr.kind.base

              
              return  ast

           #if isinstance(ast.left , Ast.FOR):
