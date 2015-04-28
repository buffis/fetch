import json
from parseractions import *
from fetchfilters import *
from requesthandler import HttpRequestHandler
from BeautifulSoup import BeautifulSoup

# TODO: Error handling on raised exceptions

FILTER_MODE_TEXT = "filter-mode-text"
FILTER_MODE_HTML = "filter-mode-html"

# Request handler that does the HTTP requests.
# Defaults to using a HTTP request handler that uses the requests library, but can be mocked out
# for tests.
REQUEST_HANDLER = HttpRequestHandler()

def inject_requesthandler_for_test(handler):
    global REQUEST_HANDLER
    REQUEST_HANDLER = handler

class InterpreterException(Exception):
    def __init__(self, msg):
        return Exception.__init__(self, msg)

class HtmlWrapper(object):
    def __init__(self, soups):
        self.soups = soups

    def filter(self, exp):
        if exp.mode != FILTER_MODE_HTML:
            raise InterpreterException("Expected HTML based filter.")
        filtered_soups = []
        for soup in self.soups:
            children = soup.findChildren(recursive=exp.f.recursive)
            matching_children = filter(exp.f, children)
            filtered_soups += matching_children  # No children were harmed making this soup.
        return HtmlWrapper(filtered_soups)

    def map(self, exp):
        if exp.mode != FILTER_MODE_HTML:
            raise InterpreterException("Expected HTML based filter.")
        text_lines = []
        for soup in self.soups:
            text_lines.append(exp.f(soup))
        return TextWrapper(text_lines)

    def output(self):
        raise InterpreterException("HTML needs to be text-filtered for output.")

    def as_text(self):
        raise NotImplementedError("Not possible currently")

class TextWrapper(object):
    def __init__(self, lines):
        self.lines = lines

    def filter(self, exp):
        if exp.mode == FILTER_MODE_TEXT:
            return TextWrapper(filter(exp.f, self.lines))
        if exp.mode == FILTER_MODE_HTML:
            return self.as_html().filter(exp)

    def map(self, exp):
        if exp.mode == FILTER_MODE_TEXT:
            return TextWrapper(map(exp.f, self.lines))
        if exp.mode == FILTER_MODE_HTML:
            return self.as_html().map(exp)

    def output(self):
        return self.lines

    def as_html(self):
        return HtmlWrapper([BeautifulSoup("".join(self.lines))])

    def __add__(self, other):  # TODO: is this needed?
        return TextWrapper(self.output() + other.output())

    def __getitem__(self, item):  # TODO: is this needed?
        pos = int(item)
        if pos > (len(self.lines) - 1):
            raise InterpreterException("Position %d is out of range" % pos)
        return TextWrapper([self.output()[pos]])

    def __str__(self):
        return str(self.lines)

class UrlWrapper(object):
    def __init__(self, method, url):
        self.method = method
        self.url = url
        self.params = {}
        self.headers = {}
        self.cookies = {}
        self.text_wrapper = None
        
    def do_request(self):
        global REQUEST_HANDLER
        if self.method == "GET":
            req = REQUEST_HANDLER.get(self.url,
                                      params=self.params,
                                      headers=self.headers,
                                      cookies=self.cookies)
        elif self.method == "POST":
            req = REQUEST_HANDLER.post(self.url,
                                       params=self.params,
                                       headers=self.headers,
                                       cookies=self.cookies)
        else:
            raise InterpreterException("Illegal request method: " + self.method)

        self.text_wrapper = TextWrapper(req.split('\n'))

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
        raise InterpreterException("Invalid field: " + action.method)
    getattr(VARS[action.name], field)[action.key] = action.value.strip("'")
    
###################### END FETCH SECTION ###################### 

####################### FILTER SECTION ########################

class FilterWrapper(object):
    def __init__(self, f, mode):
        self.f = f
        self.mode = mode

    def negated(self):
        f = self.f
        return FilterWrapper(lambda x: not f(x), self.mode)

    def and_expression(self, exp):
        f1, f2 = self.f, exp.f
        return FilterWrapper(lambda x: f1(x) and f2(x), self.mode)

    def or_expression(self, exp):
        f1, f2 = self.f, exp.f
        return FilterWrapper(lambda x: f1(x) or f2(x), self.mode)

def filter_expression(exp, filter_map):
    t = type(exp)
    if t == BasicFilterExpression:
        filter_f, mode = filter_map[exp.key]
        f = filter_f(exp.arg.strip("'") if exp.arg else '')
        return FilterWrapper(f, mode)
    if t == NegFilterExpression:
        return filter_expression(exp.exp, filter_map).negated()
    if t == CombinedFilterExpression:
        f1 = filter_expression(exp.exp1, filter_map)
        f2 = filter_expression(exp.exp2, filter_map)
        if exp.op == "|": return f1.or_expression(f2)
        if exp.op == "&": return f1.and_expression(f2)

def coarsefilteraction(action):
    coarse_filter_map = {
        "starts":    (starts_filter, FILTER_MODE_TEXT),
        "ends":      (ends_filter, FILTER_MODE_TEXT),
        "contains":  (contains_filter, FILTER_MODE_TEXT),
        "matches":   (matches_filter, FILTER_MODE_TEXT),
        "length":    (length_filter, FILTER_MODE_TEXT),
        "children":  (children_filter, FILTER_MODE_HTML),
        "findall":   (findall_filter, FILTER_MODE_HTML),
    }
    f = filter_expression(action.expression, coarse_filter_map)
    VARS[action.name] = VARS[action.indata].filter(f)

def finefilteraction(action):
    fine_filter_map = {
        "after":     (after_filter, FILTER_MODE_TEXT),
        "before":    (before_filter, FILTER_MODE_TEXT),
        "afterpos":  (afterpos_filter, FILTER_MODE_TEXT),
        "beforepos": (beforepos_filter, FILTER_MODE_TEXT),
        "exclude":   (exclude_filter, FILTER_MODE_TEXT),
        "striptags": (striptags_filter, FILTER_MODE_TEXT),
        "text":      (text_filter, FILTER_MODE_HTML),
        "rawtext":   (rawtext_filter, FILTER_MODE_HTML),
        "attr":      (attr_filter, FILTER_MODE_HTML),
    }
    f = filter_expression(action.expression, fine_filter_map)
    VARS[action.name] = VARS[action.indata].map(f)

##################### END FILTER SECTION #######################

####################### OUTPUT SECTION #########################

def outputassignment(action):
    if type(action.name) == str:
        VARS[action.name] = outputassignment_right(action.value)
    elif type(action.name) == DictAt:
        VARS[action.name.d][action.name.at.strip("'")] = outputassignment_right(action.value)
    else:
        raise InterpreterException("Unknown type: " + str(type(action.name)))

def outputassignment_right(value):
    if type(value) == ListPlus:
        return outputassignment_right(value.l1) + outputassignment_right(value.l2)
    elif type(value) == ListAt:
        return VARS[value.l][value.at]
    elif type(value) == dict:
        return_dict = {}
        for k, v in value.items():
            return_dict[k.strip("'")] = VARS[v]
        return return_dict
    elif type(value) == str:
        return VARS[value]
    else:
        raise InterpreterException("Unknown type: " + str(type(value)))

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

def get_output(mode="json"):  #shittycode
    def json_format(output):
        return json.dumps(output,
                          sort_keys=False,
                          indent=2,
                          separators=(',', ': '))
    def text_format(output, inline=False):  #shittycode
        if type(output) == list:
            if inline: return "[%s]" % ", ".join(map(text_format, output))
            else: return "\n".join(text_format(o, True) for o in output)
        elif type(output) in (str, unicode): return output
        elif type(output) == dict:
            if inline: return "{%s}" % ", ".join("%s: %s"%(k, text_format(v, True)) for (k,v) in output.items())
            else: return "{\n%s\n}" % "\n".join("%s: %s"%(k, text_format(v, True)) for (k,v) in output.items())
    def prepare_output(var):
        if type(var) == TextWrapper:
            return var.output()
        elif type(var) == dict:
            d = {}
            for key, value in var.items():
                d[key] = prepare_output(value)
            return d

    formatted_output = prepare_output(VARS['output'])
    if mode == "json":
        return json_format(formatted_output)
    elif mode == "text":
        return text_format(formatted_output)
    else:
        raise SyntaxError("Invalid mode: " + mode)
