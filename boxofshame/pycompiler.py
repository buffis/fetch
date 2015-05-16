from parseractions import *

def compile_deps():
    return """import requests,re
class TextWrapper(object):
    def __init__(self, lines):
        self.lines = lines

    def filter(self, exp):
        return TextWrapper(filter(exp, self.lines))

    def map(self, exp):
        return TextWrapper(map(exp, self.lines))

    def output(self):
        return self.lines

class UrlWrapper(object):
    def __init__(self, method, url):
        self.method = method
        self.url = url
        self.params = {}
        self.headers = {}
        self.cookies = {}
        self.text_wrapper = None
        
    def do_request(self):
        req = requests.get(self.url,
                           params=self.params,
                           headers=self.headers,
                           cookies=self.cookies)
        if req.status_code != 200:
             print "FAILED"
             return
        self.text_wrapper = TextWrapper(req.text.split('\\n'))

    def filter(self, exp):
        if not self.text_wrapper:
            self.do_request()
        return self.text_wrapper.filter(exp)

    def map(self, exp):
        if not self.text_wrapper:
            self.do_request()
        return self.text_wrapper.map(exp)

def striptags(x, v):
    tags = v.split(",")
    subbed = x
    for tag in tags:
        subbed = re.sub(r'<%s.*?>.*?</%s>' % (tag, tag), '', subbed)
        subbed = re.sub(r'<%s.*?/>' % tag, '', subbed)
    return subbed
"""

def compile_finish():
    return "print out"

######################## FETCH SECTION ######################## 

def compile_fetchaction(action):
    return "%s = UrlWrapper('%s', %s)" % (
        action.name, action.method, action.url)

def compile_modifyurlaction(action):
    field_map = {
        "PARAM"  : "params",
        "HEADER" : "headers",
        "COOKIE" : "cookies"}
    field = field_map.get(action.method, None)
    if field is None:
        raise SyntaxError("Invalid field: " + action.method)
    return "%s.%s['%s'] = %s" % (action.name, field, action.key, action.value)
    
###################### END FETCH SECTION ###################### 


####################### FILTER SECTION ########################

# TODO: Enforce validation?
def compile_starts_filter(arg): return "x.startswith(%s)" % arg
def compile_ends_filter(arg): return "x.endswith(%s)" % arg
def compile_contains_filter(arg): return "%s in x" % arg
def compile_length_filter(arg): return "len(x) %s" % arg.strip("'")
def compile_matches_filter(arg): return "re.compile(r%s).match(x)" % arg

def compile_after_filter(arg):
    return "x[x.find(%s)+%d:] if %s in x else ''" % (arg, len(arg)-2, arg)
def compile_before_filter(arg):
    return "x[:x.find(%s)] if %s in x else x" % (arg, arg)
def compile_afterpos_filter(arg): return "x[%s:]" % arg.strip("'")
def compile_beforepos_filter(arg): return "x[:%s]" % arg.strip("'")
def compile_exclude_filter(arg): return "x.replace(%s, '')" % arg
def compile_striptags_filter(arg): return "striptags(x, %s)" % arg

def compile_text_filter(_):  # TODO: FIX
    return "x"

def compile_filter_expression(exp, filter_map):
    t = type(exp)
    if t == BasicFilterExpression:
        return filter_map[exp.key](exp.arg)
    if t == NegFilterExpression:
        return "not (%s)" % compile_filter_expression(exp.exp,
                                                      filter_map)
    if t == CombinedFilterExpression:
        if exp.op == "&":
            return "(%s) and (%s)" % (compile_filter_expression(exp.exp1,
                                                                filter_map),
                                      compile_filter_expression(exp.exp2,
                                                                filter_map))
        if exp.op == "|":
            return "(%s) or (%s)" % (compile_filter_expression(exp.exp1,
                                                               filter_map),
                                      compile_filter_expression(exp.exp2,
                                                                filter_map))

def compile_coarsefilteraction(action):
    coarse_filter_map = {
        "starts" : compile_starts_filter,
        "ends" : compile_ends_filter,
        "contains" : compile_contains_filter,
        "length" : compile_length_filter,
        "matches" : compile_matches_filter,
    }
    exp = "lambda x: " + compile_filter_expression(action.expression,
                                                   coarse_filter_map)
    return "%s = %s.filter(%s)" % (action.name, action.indata, exp)

def compile_finefilteraction(action):
    fine_filter_map = {
        "after" : compile_after_filter,
        "before" : compile_before_filter,
        "afterpos" : compile_after_filter,
        "beforepos" : compile_before_filter,
        "text" : compile_text_filter,
        "exclude" : compile_exclude_filter,
        "striptags" : compile_striptags_filter,
    }
    exp = "lambda x: " + compile_filter_expression(action.expression,
                                                   fine_filter_map)
    return "%s = %s.map(%s)" % (action.name, action.indata, exp)

##################### END FILTER SECTION #######################
    
####################### OUTPUT SECTION #########################

def compile_outputassignment(action):
    return str(action.name) + "=" + compile_outputassignment_right(action.value)

def compile_outputassignment_right(value):
    if type(value) == ListPlus:
        return "%s + %s" % (compile_outputassignment_right(value.l1),
                            compile_outputassignment_right(value.l2))
    if type(value) == ListAt:
        return "%s.output()[%s]" % (value.l, value.at)
    if type(value)== dict:
        # TODO: Clean up.
        return "{" + ", ".join(["%s : %s.output()" % (x,y) for (x,y) in value.items()]) + "}"
    if type(value) == str:
        return "%s.output()" % value

##################### END OUTPUT SECTION #######################

def compile_line(line):
    compile_map = {
        FetchAction : compile_fetchaction,
        ModifyUrlAction : compile_modifyurlaction,
        CoarseFilterAction : compile_coarsefilteraction,
        FineFilterAction : compile_finefilteraction,
        OutputAssignment : compile_outputassignment
    }
    return compile_map[type(line)](line) + "\n"
