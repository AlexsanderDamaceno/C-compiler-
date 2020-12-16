from enum import Enum


class Ast_Type():
	NUMBER           = 0
	PLUS             = 1
	SUB              = 2
	MUL              = 3
	DIV              = 4
	LESS             = 5
	LESS_EQUAL       = 6
	GREATER          = 7
	GREATER_EQUAL    = 8
	NEG              = 9
	EQUAL_EQUAL      = 10
	NOT_EQUAL        = 11
	EXPR_STMT        = 12
	ID               = 13
	ASSIGN           = 14
	RETURN           = 15
	COMPOUND_STMT    = 16
	IF               = 17
	FOR              = 18
	DEREF            = 19
	ADDR             = 20
	AST_FUNCALL      = 21

class Ast_TypeKind():
   TY_INT       = 1
   TY_POINTER   = 2
   TY_FUNCTION  = 3
   TY_ARRAY     = 4




class Ast():
	pass


class Function_Call():
   def __init__(self, name , args):
	    self.name = name
	    self.args = args


class Function(Ast):
	def __init__(self, func_name , params , ty , body  , locals):
		self.func_name  = func_name
		self.params     = params
		self.ty         = ty
		self.body       = body
		self.locals     = locals
		self.stack_size = 0


class Object():
  def __init__(self , name , ty):
  	   self.ty     =  ty


class Decl():
	def __init__(self , name , ty):
	  self.name   = name
	  self.ty     = ty
	  self.offset = -1

class Identifier(Ast):

  def __init__(self ,  name  , decl):
  	 self.name   = name
  	 self.kind   = decl.ty
  	 self.Decl   = decl





class Compound_stmt(Ast):

  def __init__(self , type , stmt_list):
  	 #self.type = type
	 #self.stmt_list = stmt_list
     self.type = type
     self.stmt_list = stmt_list




class Assign(Ast):

  def __init__(self , left , type  , right):
  	  self.left    = left
  	  self.type    = type
  	  self.right   = right



class BinOp(Ast):

  def __init__(self , left , type  , right):
  	  self.left    = left
  	  self.type    = type
  	  self.right   = right
  	  self.kind    = None


class Unary(Ast):

  def __init__(self , type  ,  expr):
  	  self.type    = type
  	  self.expr    = expr
  	  self.kind    = None


class For(Ast):
  def __init__(self , type ,  init , cond , inc , body):
        self.type = type
        self.init = init
        self.cond = cond
        self.inc  = inc
        self.body = body


class If(Ast):
  def __init__(self , type ,  cond , then , els):
        self.type = type
        self.cond = cond
        self.then = then
        self.els  = els




class Num(Ast):

  def __init__(self ,  value):
	   self.value  = value
	   self.kind   = None


class Type(Ast):
  def __init__(self ,  type  , base , size):
  	self.type = type
  	self.base = base
  	self.size = size
  	self.array_len = 0
  	self.name = None
