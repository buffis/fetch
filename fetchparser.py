import ply.yacc as yacc

from fetchlexer import tokens
from parseractions import *

############
# Main rules
##########

def p_fetchsection(p):
    """fetchcode : fetchlines"""
    p[0] = p[1]

def p_fetchlines(p):
    """fetchlines : fetchline fetchlines
                  | fetchline"""
    p[0] = [p[1]]
    if len(p) > 2:
        p[0] += p[2]

def p_fetchline_modify(p):
    """fetchline : requestline
                 | paramline
                 | headerline
                 | cookieline
                 | filterline
                 | outputline"""
    p[0] = p[1]

def p_error(p):
    "Error in syntax"
    print "Error parsing expression: %s at line %d" % (p.value, p.lineno)
    raise SyntaxError()


############
# Fetch section
##########

def p_get(p):
    "get : LARROW"
    p[0] = "GET"

def p_post(p):
    "post : RARROW"
    p[0] = "POST"

def p_fetchline_fetch(p):
    """requestline : NAME get  STRING NEWLINE
                   | NAME post STRING NEWLINE"""
    p[0] = FetchAction(p[1], p[2], p[3])
    
def p_paramline(p):
    """paramline : NAME LBRACE NAME RBRACE EQUALS STRING NEWLINE"""
    p[0] = ModifyUrlAction(p[1], "PARAM", p[3], p[6])

def p_headerline(p):
    """headerline : NAME LCURLY NAME RCURLY EQUALS STRING NEWLINE"""
    p[0] = ModifyUrlAction(p[1], "HEADER", p[3], p[6])

def p_cookieline(p):
    """cookieline : NAME LT NAME GT EQUALS STRING NEWLINE"""
    p[0] = ModifyUrlAction(p[1], "COOKIE", p[3], p[6])


############
# Filter section
##########

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


############
# Output section
##########

def p_outputline(p):
    """outputline : NAME EQUALS outputright NEWLINE"""
    p[0] = OutputAssignment(p[1], p[3])

def p_outputline_dict(p):
    """outputline : NAME LBRACE STRING RBRACE EQUALS outputright NEWLINE"""
    p[0] = OutputAssignment(DictAt(p[1], p[3]), p[6])

def p_outputright(p):
    """outputright : NAME
                   | STRING
                   | outputdict"""
    p[0] = p[1]

def p_outputright_arrayitem(p):
    """outputright : NAME LBRACE NUMBER RBRACE"""
    p[0] = ListAt(p[1], p[3])

def p_outputright_expression(p):
    """outputright : NAME PLUS NAME"""
    p[0] = ListPlus(p[1], p[3])

def p_outputright_list(p):
    """outputright : LBRACE outputlistitems RBRACE"""
    p[0] = p[2]
    
def p_outputlistitems_single(p):
    """outputlistitems : STRING"""
    p[0] = [p[1]]
    
def p_outputlistitems_multiple(p):
    """outputlistitems : STRING COMMA outputlistitems"""
    p[0] = [p[1]] + p[3]

def p_outputdict(p):
    """outputdict : DICT LCURLY outputdictitems RCURLY"""
    p[0] = p[3]

def p_outputdictitems_single(p):
    """outputdictitems : STRING COLON NAME"""
    p[0] = {p[1]: p[3]}
    
def p_outputdictitems_multiple(p):
    """outputdictitems : STRING COLON NAME COMMA outputdictitems"""
    d = p[5]
    d[p[1]] = p[3]
    p[0] = d


############
# API
##########

def parse_input(i):
    import fetchlexer
    parser = yacc.yacc()
    lexer = fetchlexer.get_lexer()
    result = parser.parse(i, lexer=lexer)
    return result


############
# Print parser rules
##########

if __name__ == "__main__":
    # TODO: Compare lists below with global function starting with "p_"
    rules = [
        ("Main parsing",   [p_fetchsection, p_fetchlines, p_fetchline_modify]),
        ("Fetch section",  [p_fetchline_fetch, p_paramline, p_headerline, p_cookieline, p_get, p_post]),
        ("Filter section", [p_filterline_coarse, p_filterline_fine, p_filterexpression,
                           p_filterexpression_noarg, p_filterexpression_neg, p_filterexpression_combined]),
        ("Output section", [p_outputline, p_outputline_dict, p_outputright, p_outputright_arrayitem,
                           p_outputright_expression, p_outputright_list, p_outputlistitems_single,
                           p_outputlistitems_multiple, p_outputdict, p_outputdictitems_single,
                           p_outputdictitems_multiple])]
    
    def fl(l,p):
        # TODO: Clean this up.
        if ":" in l:
            before,after = l.split(":")
            t = p-len(before)
            l = before + " "*t + ":" + after
        return ("\n" +(" "*p)).join([x.strip() for x in l.split("\n")])

    print "Fetch context-free grammar:"
    for section,rules in rules:
        print section + ":"
        for rule in rules:
            print fl(rule.__doc__, 18)
        print ""
    
