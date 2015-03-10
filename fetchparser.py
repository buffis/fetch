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

def p_fetchline_fetch(p):
    """fetchline : NAME get  STRING NEWLINE
                 | NAME post STRING NEWLINE"""
    p[0] = FetchAction(p[1], p[2], p[3])

def p_fetchline_modify(p):
    """fetchline : paramline
                 | headerline
                 | cookieline"""
    p[0] = p[1]

def p_fetchline_filter(p):
    """fetchline : filterline"""
    p[0] = p[1]
    
def p_paramline(p):
    """paramline : NAME LBRACE NAME RBRACE EQUALS STRING NEWLINE"""
    p[0] = ModifyUrlAction(p[1], "PARAM", p[3], p[6])

def p_headerline(p):
    """headerline : NAME LCURLY NAME RCURLY EQUALS STRING NEWLINE"""
    p[0] = ModifyUrlAction(p[1], "HEADER", p[3], p[6])

def p_cookieline(p):
    """cookieline : NAME LT NAME GT EQUALS STRING NEWLINE"""
    p[0] = ModifyUrlAction(p[1], "COOKIE", p[3], p[6])

def p_filterline_coarse(p):
    """filterline : NAME EQUALS LBRACE filterexpression RBRACE NAME NEWLINE"""
    p[0] = CoarseFilterAction(p[1], p[4], p[6])

def p_filterline_fine(p):
    """filterline : NAME EQUALS LCURLY filterexpression RCURLY NAME NEWLINE"""
    p[0] = FineFilterAction(p[1], p[4], p[6])

def p_filterexpression(p):
    """filterexpression : NAME COLON STRING"""
    p[0] = BasicFilterExpression(p[1], p[3])

def p_filterexpression_noarg(p):
    """filterexpression : NAME"""
    p[0] = BasicFilterExpression(p[1])

def p_filterexpression_neg(p):
    """filterexpression : BANG filterexpression"""
    p[0] = NegFilterExpression(p[2])

def p_filterexpression_combined(p):
    """filterexpression : filterexpression AND filterexpression
                        | filterexpression OR filterexpression"""
    p[0] = CombinedFilterExpression(p[1],p[3],p[2])

def p_get(p):
    "get : LARROW"
    p[0] = "GET"

def p_post(p):
    "post : RARROW"
    p[0] = "POST"

def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    print "Syntax error in input!"

def parse_input(i):
    import lexer
    parser = yacc.yacc()
    lexer = lexer.get_lexer()
    result = parser.parse(i, lexer=lexer)
    return result

class FilterExpression(object):
    pass

class NegFilterExpression(FilterExpression):
    def __init__(self, exp):
        self.exp = exp
    def __str__(self):
        return "<!Filter: " + str(self.exp) + ">"

class CombinedFilterExpression(FilterExpression):
    def __init__(self, exp1, exp2, op):
        self.exp1 = exp1
        self.exp2 = exp2
        self.op = op
    def __str__(self):
        return "<Filter: " + str(self.exp1) + str(self.op) + str(self.exp2) + ">"

class BasicFilterExpression(FilterExpression):
    def __init__(self, key, arg=None):
        self.key = key
        self.arg = arg
    def __str__(self):
        r = "<Filter:" + self.key
        if self.arg:
            r += ":" + self.arg
        return r + ">"

class FilterAction(object):
    def __init__(self, name, expression, indata):
        self.name = name
        self.expression = expression
        self.indata = indata
    def __str__(self):
        return str(type(self)) + self.name + str(self.expression) + self.indata
    def __repr__(self):
        return str(self)

class CoarseFilterAction(FilterAction):
    pass

class FineFilterAction(FilterAction):
    pass

class FetchAction(object):
    def __init__(self, name, method, url):
        self.name = name
        self.method = method
        self.url = url

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "FetchAction: " + self.name + self.method + self.url

class ModifyUrlAction(object):
    def __init__(self, name, method, key, value):
        self.name = name
        self.method = method
        self.key = key
        self.value = value

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "ModifyUrlAction: " + self.name + self.method + self.key + self.value
