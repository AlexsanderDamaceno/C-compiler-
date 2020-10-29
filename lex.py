import ply.lex as lex

tokens = (
 'NUMBER'  ,
 'PLUS'    ,
 'SUB'     ,
 'MUL'     ,
 'DIV'     ,
 'LPAREN'  ,
 'RPAREN'  ,
 'LESS' ,
 'LESS_EQUAL' ,
 'GREATER' ,
 'GREATER_EQUAL' ,
 'EQUAL_EQUAL' ,
 'NOT_EQUAL' ,
 'SEMICOLON' ,
 'ID' ,
 'ASSIGN' ,
 'RETURN' ,
 'LBRACE' ,
 'RBRACE' ,
 'IF'     ,
 'ELSE' ,
 'FOR' , 
 'WHILE' , 
 'ADDR_BIT' ,   
 'INT' , 
 'COMMA'
 
)

reserved = {
'return' : 'RETURN' ,
'if'     : 'IF' ,
'else'   : 'ELSE' ,
'for'    : 'FOR' , 
'while'  : 'WHILE' , 
'int'    : 'INT'
}


t_PLUS          = r'\+'
t_SUB           = r'\-'
t_MUL           = r'\*'
t_DIV           = r'\/'
t_ADDR_BIT      = r'\&'
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_LESS          = r'\<'
t_LESS_EQUAL    = r'\<='
t_GREATER       = r'\>'
t_GREATER_EQUAL = r'\>='
t_EQUAL_EQUAL   = r'\=='
t_NOT_EQUAL     = r'\!='
t_SEMICOLON     = r'\;'
t_ASSIGN        = r'\='
t_LBRACE        = r'\{'
t_RBRACE        = r'\}'
t_COMMA         = r'\,'

digit           = r'([0-9])'
nondigit        = r'([_A-Za-z])'




def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value , 'ID')
    return t

def t_NUMBER(t):
	r'\d+'
	return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return

def t_eof(t):
    return t

t_ignore = ' \t'

def t_error(t):
     print("Illegal character '%s'" % t.value[0])
     t.lexer.skip(1)
     return


def  make_token(file_content):
 token_list = []
 lexer = lex.lex()

 lexer.input(file_content)

 while  True:
    tok = lexer.token()

    if tok.type ==  'eof':
        token_list.append(tok)
        break
    token_list.append(tok)
 return token_list
