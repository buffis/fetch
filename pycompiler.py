from parseractions import *


def compile_deps():
    print "import requests"
    print """
class UrlWrapper(object):
    def __init__(self, method, url):
        self.method = method
        self.url = url
        self.params = {}
        self.headers = {}
        self.cookies = {}
"""

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

compile_map = {
    FetchAction : compile_fetchaction,
    ModifyUrlAction : compile_modifyurlaction
}

def compile_line(line):
    compile_map[type(line)](line)
