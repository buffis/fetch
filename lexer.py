import ply.lex as lex

reserved = {
   'dict' : 'DICT',
}

tokens = (
    # Non-trivial tokens.
    'NAME',
    'STRING',
    'NUMBER',

    # Trivial tokens.
    'LARROW',
    'RARROW',
    'EQUALS',
    'LPAREN',
    'RPAREN',
    'LCURLY',
    'RCURLY',
    'LBRACE',
    'RBRACE',
    'LT',
    'GT',
    'COLON',
    'COMMA',
    'PLUS',
    'NEWLINE',
    'BANG',
    'OR',
    'AND',

    # Reserved words.
    'DICT'
) 

# Regular expression rules for simple tokens.
t_LARROW    = r'<-'
t_RARROW    = r'->'
t_EQUALS    = r'='
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LCURLY    = r'\{'
t_RCURLY    = r'\}'
t_LBRACE    = r'\['
t_RBRACE    = r'\]'
t_COLON     = r':'
t_COMMA     = r','
t_PLUS      = r'\+'
t_LT        = r'<'
t_GT        = r'>'
t_BANG      = r'!'
t_OR        = r'\|'
t_AND       = r'&'

def t_NAME(t):
    r'[a-zA-Z]+' 
    t.type = reserved.get(t.value,'NAME')
    return t

def t_STRING(t):
    r"'[^']*'"
    return t

def t_NUMBER(t):
    r'\d+'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.type = "NEWLINE"
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

# Ignored characters.
t_ignore  = ' \t'

# Error handling rule.
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

def get_lexer():
    return lex.lex()
