from parseractions import *

def compile_deps():
    print "import requests"
    print """
class TextWrapper(object):
    def __init__(self, lines):
        self.lines = lines

    def apply_filter(self, exp):
        pass

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

    def apply_filter(self, exp):
        if not self.text_wrapper:
            self.do_request()
        wrapper = self.text_wrapper:
"""

######################## FETCH SECTION ######################## 

def compile_fetchaction(action):
    print "%s = UrlWrapper('%s', %s)" % (
        action.name, action.method, action.url)

def compile_modifyurlaction(action):
    field_map = {
        "PARAM"  : "params",
        "HEADER" : "headers",
        "COOKIE" : "cookies"}
    field = field_map.get(action.method, None)
    if field is None:
        raise SyntaxError("Invalid field: " + action.method)
    print "%s.%s['%s'] = %s" % (action.name, field, action.key, action.value)
    
###################### END FETCH SECTION ###################### 


####################### FILTER SECTION ########################

def compile_starts_filter(arg): return "x.startswith(%s)" % arg
def compile_ends_filter(arg): return "x.endswith(%s)" % arg
def compile_contains_filter(arg): return "x.contains(%s)" % arg
    

def compile_filter_expression(exp, filter_map):
    t = type(exp)
    if t == BasicFilterExpression:
        return filter_map[exp.key](exp.arg)
    if t == NegFilterExpression:
        return "not (%s)" % compile_filter_expression(exp.exp,
                                                      filter_map)
    if t == CombinedFilterExpression:
        if exp.op == "&":
            return "(%s) AND (%s)" % (compile_filter_expression(exp.exp1,
                                                                filter_map),
                                      compile_filter_expression(exp.exp2,
                                                                filter_map))
        if exp.op == "|":
            return "(%s) OR (%s)" % (compile_filter_expression(exp.exp1,
                                                               filter_map),
                                      compile_filter_expression(exp.exp2,
                                                                filter_map))

def compile_coarsefilteraction(action):
    coarse_filter_map = {
        "starts" : compile_starts_filter,
        "ends" : compile_ends_filter,
        "contains" : compile_contains_filter,
    }
    print "lambda x: " + compile_filter_expression(action.expression,
                                                   coarse_filter_map)

##################### END FILTER SECTION #######################
    
def compile_line(line):
    compile_map = {
        FetchAction : compile_fetchaction,
        ModifyUrlAction : compile_modifyurlaction,
        CoarseFilterAction : compile_coarsefilteraction,
    }
    compile_map[type(line)](line)
