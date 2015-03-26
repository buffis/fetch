from parseractions import *
from fetchfilters import *
import requests

# TODO: Error handling on raised exceptions

class TextWrapper(object):
    def __init__(self, lines):
        self.lines = lines

    def filter(self, exp):
        return TextWrapper(filter(exp, self.lines))

    def map(self, exp):
        return TextWrapper(map(exp, self.lines))

    def output(self):
        return self.lines

    def __add__(self, other):
        return TextWrapper(self.output() + other.output())

    def __getitem__(self, item):
        pos = int(item)
        if pos > (len(self.lines) - 1):
            raise SyntaxError("Position %d is out of range" % pos)
        return TextWrapper([self.output()[pos]])

class UrlWrapper(object):
    def __init__(self, method, url):
        self.method = method
        self.url = url
        self.params = {}
        self.headers = {}
        self.cookies = {}
        self.text_wrapper = None
        
    def do_request(self):
        # TODO: Handle POST
        if self.method == "GET":
            req = requests.get(self.url,
                               params=self.params,
                               headers=self.headers,
                               cookies=self.cookies)
        elif self.method == "POST":
            req = requests.post(self.url,
                                params=self.params,
                                headers=self.headers,
                                cookies=self.cookies)
        else:
            raise SyntaxError("Illegal request method: " + self.method)

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

def filter_expression(exp, filter_map):
    # TODO: Verify neg/or/and coarse filter only is possible (or do in parser).
    t = type(exp)
    if t == BasicFilterExpression:
        return filter_map[exp.key](exp.arg.strip("'"))
    if t == NegFilterExpression:
        return lambda x: not filter_expression(exp.exp, filter_map)(x)
    if t == CombinedFilterExpression:
        f1 = filter_expression(exp.exp1, filter_map)
        f2 = filter_expression(exp.exp2, filter_map)
        if exp.op == "|": return lambda x: f1(x) or f2(x)
        if exp.op == "&": return lambda x: f1(x) and f2(x)

def coarsefilteraction(action):
    coarse_filter_map = {
        "starts" : starts_filter,
        "ends" : ends_filter,
        "contains" : contains_filter,
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
        "exclude" : exclude_filter,
        "striptags" : striptags_filter,
        #"text" : text_filter, # TODO: Implement
    }
    f = filter_expression(action.expression, fine_filter_map)
    VARS[action.name] = VARS[action.indata].map(f)

##################### END FILTER SECTION #######################

####################### OUTPUT SECTION #########################

def outputassignment(action):
    if type(action.name) == str:
        VARS[action.name] = outputassignment_right(action.value)
    elif type(action.name) == DictAt:
        VARS[action.name.d][action.name.at] = outputassignment_right(action.value)
    else:
        raise SyntaxError("Unknown type: " + str(type(action.name)))

def outputassignment_right(value):
    if type(value) == ListPlus:
        return outputassignment_right(value.l1) + outputassignment_right(value.l2)
    elif type(value) == ListAt:
        return VARS[value.l][value.at]
    elif type(value) == dict:
        return_dict = {}
        for k, v in value.items():
            return_dict[k] = VARS[v]
        return return_dict
    elif type(value) == str:
        return VARS[value]
    else:
        raise SyntaxError("Unknown type: " + str(type(value)))

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
