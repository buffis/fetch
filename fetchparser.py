import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lexer import tokens

def p_fetchsection(p):
    """fetchsection : fetchlines"""
    p[0] = p[1]
        
def p_fetchlines(p):
    """fetchlines : fetchline fetchlines
                  | fetchline"""
    p[0] = [p[1]]
    if len(p) > 2:
        p[0] += p[2]

def p_fetchline(p):
    """fetchline : name get  url NEWLINE
                 | name post url NEWLINE
                 | paramline
                 | headerline
                 | cookieline"""
    if len(p) > 2:
        p[0] = FetchAction(p[1], p[2], p[3])
    else:
        p[0] = p[1:]

def p_paramline(p):
    """paramline : name LBRACE name RBRACE EQUALS STRING NEWLINE"""
    p[0] = p[1:7]

def p_headerline(p):
    """headerline : name LCURLY name RCURLY EQUALS STRING NEWLINE"""
    p[0] = p[1:7]

def p_cookieline(p):
    """cookieline : name LT name GT EQUALS STRING NEWLINE"""
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
    print "Syntax error in input!" + p

def parse_input(i):
    import lexer
    parser = yacc.yacc()
    lexer = lexer.get_lexer()
    result = parser.parse(i, lexer=lexer)
    return result


class FetchAction(object):
    def __init__(self, name, method, url):
        self.name = name
        self.method = method
        self.url = url

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "FetchAction: " + self.name + self.method + self.url

