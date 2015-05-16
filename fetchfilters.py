import re

# TODO: Add docstring explaining coarse/fine filters and modes.
# TODO: Enforce validation.


# Coarse text filters:
def starts_filter(arg):
    return lambda x: x.startswith(arg)


def ends_filter(arg):
    return lambda x: x.endswith(arg)


def contains_filter(arg):
    return lambda x: arg in x


def matches_filter(arg):
    return lambda x: re.compile(arg).match(x)


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
    # TODO: Handle error


# Fine text filters:
def after_filter(arg):
    return lambda x: x[x.find(arg) + len(arg):] if arg in x else ''


def before_filter(arg):
    return lambda x: x[:x.find(arg)] if arg in x else x


def afterpos_filter(arg):
    return lambda x: x[int(arg):]


def beforepos_filter(arg):
    return lambda x: x[:int(arg)]


def exclude_filter(arg):
    return lambda x: x.replace(arg, '')


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
def _match_tag(arg):
    """
    Helper method for "children" and "findall" filters, used to match a tag.
    Expects a tag name and/or class. If class is specified, a dot is used as separator.
    Example inputs: "p", "img", "span.classname", "img.header", ".repo".
    """
    if "." in arg:
        name, cls = arg.split(".")
    else:
        # No class specified. Just a tag.
        name = arg
        cls = None

    def f(x):
        if name:
            matching_name = x.name == name
        else:
            matching_name = True
        if cls:
            try:
                matching_class = cls in x["class"].split()
                return matching_name and matching_class
            except KeyError:
                return False  # No class!
        else:
            return matching_name
    return f


def children_filter(arg):
    f = _match_tag(arg)
    f.recursive = False
    return f


def findall_filter(arg):
    f = _match_tag(arg)
    f.recursive = True
    return f


# Fine HTML filters:
def text_filter(_):
    return lambda x: x.getText()


def rawtext_filter(_):
    return lambda x: str(x)


def attr_filter(arg):
    def f(x):
        try:
            return x[arg]
        except KeyError:
            return ""
    return f
