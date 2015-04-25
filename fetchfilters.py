import re

# TODO: Add docstring explaining coarse/fine filters and modes.
# TODO: Enforce validation.

# Coarse text filters:
def starts_filter(arg): return lambda x: x.startswith(arg)

def ends_filter(arg): return lambda x: x.endswith(arg)

def contains_filter(arg): return lambda x: arg in x

def matches_filter(arg): return lambda x: re.compile(arg).match(x)

def length_filter(arg):
    def t(x):
        tmp = re.search(r"<(\d+)", arg)
        if tmp:
            return len(x) < int(tmp.groups()[0])
        tmp = re.search(r">(\d+)", arg)
        if tmp:
            return len(x) > int(tmp.groups()[0])
        tmp = re.search(r"=(\d+)", arg)
        if tmp:
            return len(x) == int(tmp.groups()[0])
        print "Invalid input to length filter: ", arg
    return t
    #TODO: Handle error

# Fine text filters:
def after_filter(arg): return lambda x: x[x.find(arg)+len(arg):] if arg in x else ''

def before_filter(arg): return lambda x: x[:x.find(arg)] if arg in x else x

def afterpos_filter(arg): return lambda x: x[int(arg):]

def beforepos_filter(arg): return lambda x: x[:int(arg)]

def exclude_filter(arg): return lambda x: x.replace(arg, '')

def striptags_filter(arg):
    def striptags(x, v):
        tags = v.split(",")
        subbed = x
        for tag in tags:
            subbed = re.sub(r'<%s.*?>.*?</%s>' % (tag, tag), '', subbed)
            subbed = re.sub(r'<%s.*?/>' % tag, '', subbed)
        return subbed
    return lambda x: striptags(x, arg)

# Coarse HTML filters:
def children_filter(arg):
    f = lambda x: x.name == arg
    f.recursive = False
    return f

def findall_filter(arg):
    f = lambda x: x.name == arg
    f.recursive = True
    return f

# Fine HTML filters:
def text_filter(_): return lambda x: x.getText()

def rawtext_filter(_): return lambda x: str(x)

def attr_filter(arg):
    def f(x):
        try:
            return x[arg]
        except KeyError:
            return ""
    return f

