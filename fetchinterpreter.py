from parseractions import *
from fetchfilters import *
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
# TODO: Refactor filter maps

def filter_expression(exp, filter_map):
    t = type(exp)
    if t == BasicFilterExpression:
        return filter_map[exp.key](exp.arg.strip("'"))
    # TODO: non-basic filtering

def coarsefilteraction(action):
    coarse_filter_map = {
        "starts" : starts_filter,
        "ends" : ends_filter,
        "containts" : contains_filter,
        "matches" : matches_filter,
        "length" : length_filter,
    }
    f = filter_expression(action.expression, coarse_filter_map)
    VARS[action.name] = VARS[action.indata].filter(f)

def finefilteraction(action):
    fine_filter_map = {
        "after" : after_filter,
        "before" : before_filter,
        "afterpos" : afterpos_filter,
        "beforepos" : beforepos_filter,
        "text" : text_filter,
        "exclude" : exclude_filter,
        "striptags" : striptags_filter,
    }
    f = filter_expression(action.expression, fine_filter_map)
    VARS[action.name] = VARS[action.indata].map(f)

##################### END FILTER SECTION #######################

####################### OUTPUT SECTION #########################

def outputassignment(action):
    # only simple vars so far
    VARS[action.name] = outputassignment_right(action.value)

def outputassignment_right(value):
    if (type(value) == ListPlus):
        return outputassignment_right(value.l1) + outputassignment_right(value.l2)
    if (type(value) == ListAt):
        return value.l.output()[value.at]
    if type(value)== dict:
        pass
        #TODO: Implement.
        #return "{" + ", ".join(["%s : %s.output()" % (x,y) for (x,y) in value.items()]) + "}"
    if type(value) == str:
        return VARS[value].output()

##################### END OUTPUT SECTION #######################


def handle_line(line):
    action_map = {
        FetchAction : fetchaction,
        ModifyUrlAction : modifyurlaction,
        CoarseFilterAction : coarsefilteraction,
        FineFilterAction : finefilteraction,
        OutputAssignment : outputassignment,
    }
    action_map[type(line)](line)
    print "Handled: ", line

def get_output():
    return VARS['output']
