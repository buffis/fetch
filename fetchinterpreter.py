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

def striptags(x, v):
    tags = v.split(",")
    subbed = x
    for tag in tags:
        subbed = re.sub(r'<%s.*?>.*?</%s>' % (tag, tag), '', subbed)
        subbed = re.sub(r'<%s.*?/>' % tag, '', subbed)
    return subbed

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
def ends_filter(arg): return lambda x: x.endswith(arg)
def contains_filter(arg): return lambda x: s in arg
def matches_filter(arg): return lambda x: re.compile(arg).match(x)
# TODO: def length_filter(arg): return lambda x: len(x) arg

def after_filter(arg): return lambda x: x[x.find(arg)+len(arg)-2:] if arg in x else ''
def before_filter(arg): return lambda x: x[:x.find(arg)] if arg in x else x
def afterpos_filter(arg): return lambda x: x[arg:]
def beforepos_filter(arg): return lambda x: x[:arg]
def exclude_filter(arg): return lambda x: x.replace(arg, '')
def striptags_filter(arg): return lambda x: striptags(x, arg)

def text_filter(arg): return lambda x: x #TODO

def filter_expression(exp, filter_map):
    t = type(exp)
    if t == BasicFilterExpression:
        return filter_map[exp.key](exp.arg.strip("'"))

def coarsefilteraction(action):
    coarse_filter_map = {
        "starts" : starts_filter,
        "ends" : ends_filter,
        "containts" : contains_filter,
        "matches" : matches_filter,
        #"length" : length_filter, TODO
    }
    f = filter_expression(action.expression, coarse_filter_map)
    VARS[action.name] = VARS[action.indata].filter(f)

def finefilteraction(action):
    fine_filter_map = {
        "after" : after_filter,
        "before" : before_filter,
        "afterpos" : after_filter,
        "beforepos" : before_filter,
        "text" : text_filter,
        "exclude" : exclude_filter,
        "striptags" : striptags_filter,
    }
    f = filter_expression(action.expression, fine_filter_map)
    VARS[action.name] = VARS[action.indata].filter(f)

##################### END FILTER SECTION #######################

def handle_line(line):
    action_map = {
        FetchAction : fetchaction,
        ModifyUrlAction : modifyurlaction,
        CoarseFilterAction : coarsefilteraction,
        FineFilterAction : finefilteraction,
        OutputAssignment : lambda x: x,
    }
    action_map[type(line)](line)
    print "Handled: ", line
