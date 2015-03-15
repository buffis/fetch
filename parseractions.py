"""
Actions representing nodes in the parse tree.
"""

class ParserAction(object):
    pass

class ListPlus(object):
    def __init__(self, l1, l2):
        self.l1 = l1
        self.l2 = l2
    def __str__(self):
        return "%s + %s" % (str(self.l1), str(self.l2))

class DictAt(object):
    def __init__(self, d, at):
        self.d = d
        self.at = at
    def __str__(self):
        return "%s[%s]" % (str(self.d), str(self.at))
    
class ListAt(object):
    def __init__(self, l, at):
        self.l = l
        self.at = at
    def __str__(self):
        return "%s[%s]" % (str(self.l), str(self.at))

class OutputAssignment(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __str__(self):
        return "Assignment: " + str(self.name) + " = " + str(self.value)

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
        return "Filter: " + str(type(self)) + self.name + str(self.expression) + self.indata
    def __repr__(self):
        return str(self)

class CoarseFilterAction(FilterAction):
    pass

class FineFilterAction(FilterAction):
    pass

class FetchAction(ParserAction):
    def __init__(self, name, method, url):
        self.name = name
        self.method = method
        self.url = url
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
