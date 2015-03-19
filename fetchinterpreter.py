from parseractions import *
import requests,re

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
        self.text_wrapper = TextWrapper(req.text.split('\n'))

    def filter(self, exp):
        if not self.text_wrapper:
            self.do_request()
        return self.text_wrapper.filter(exp)

    def map(self, exp):
        if not self.text_wrapper:
            self.do_request()
        return self.text_wrapper.map(exp)


VARS = {}

######################## FETCH SECTION ######################## 

def fetchaction(action):
    VARS[action.name] = UrlWrapper(action.method, action.url.strip("'"))

def modifyurlaction(action):
    field_map = {
        "PARAM"  : "params",
        "HEADER" : "headers",
        "COOKIE" : "cookies"}
    field = field_map.get(action.method, None)
    if field is None:
        raise SyntaxError("Invalid field: " + action.method)
    getattr(VARS[action.name], field)[action.key] = action.value.strip("'")
    
###################### END FETCH SECTION ###################### 

####################### FILTER SECTION ########################

# TODO: Enforce validation?
def starts_filter(arg): return lambda x: x.startswith(arg)

def filter_expression(exp, filter_map):
    t = type(exp)
    if t == BasicFilterExpression:
        return filter_map[exp.key](exp.arg.strip("'"))

def coarsefilteraction(action):
    coarse_filter_map = {
        "starts" : starts_filter,
    }
    f = filter_expression(action.expression, coarse_filter_map)
    VARS[action.name] = VARS[action.indata].filter(f)

##################### END FILTER SECTION #######################

def handle_line(line):
    action_map = {
        FetchAction : fetchaction,
        ModifyUrlAction : modifyurlaction,
        CoarseFilterAction : coarsefilteraction,
        FineFilterAction : lambda x: x,
        OutputAssignment : lambda x: x,
    }
    action_map[type(line)](line)
    print "Handled: ", line
