import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lexer import tokens

def p_fetchsection(p):
    """fetchsection : fetchsectionline fetchsection
                    | empty"""
    if p[1]: # not empty
        p[0] = p[2] + [p[1]]
    else:
        p[0] = []
    

def p_fetchsectionline(p):
    """fetchsectionline : fetchline
                        | paramline"""
    p[0] = p[1]

def p_fetchline(p):
    """fetchline : name get  url NEWLINE
                 | name post url NEWLINE"""
    p[0] = p[1] + p[2] + p[3]

def p_paramline(p):
    """paramline : name LBRACE name RBRACE EQUALS STRING NEWLINE"""
    p[0] = p[1:7]

def p_name(p):
    "name : NAME"
    p[0] = p[1]

def p_url(p):
    "url : STRING"
    p[0] = p[1]

def p_get(p):
    "get : LARROW"
    p[0] = "GET"

def p_post(p):
    "post : RARROW"
    p[0] = "POST"

def p_empty(p):
    'empty :'
    p[0] = None


# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"

def parse_input(i):
    import lexer
    parser = yacc.yacc()
    lexer = lexer.get_lexer()
    result = parser.parse(i, lexer=lexer)
    return result
