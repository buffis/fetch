import re

# TODO: Add docstring explaining coarse/fine filters and modes.


class FilterException(Exception):
    def __init__(self, msg, f):
        filter_name = f.func_name[:f.func_name.rfind("_filter")]  #shittycode
        self.msg = "Filter '%s' failed validation: %s" % (filter_name, msg)


# Validators
def needs_empty_string(f):
    def t(x):
        if not x:
            return f(x)
        else:
            raise FilterException("Needs empty string", f)
    return t


def needs_nonempty_string(f):
    def t(x):
        if not x:
            raise FilterException("Needs nonempty string", f)
        else:
            return f(x)
    return t


def needs_regex(f):
    def t(x):
        try:
            re.compile(x)
            return f(x)
        except:
            raise FilterException("Invalid regex", f)
    return t


def needs_number(f):
    def t(x):
        try:
            re.compile(x)
            return f(x)
        except:
            raise FilterException("Invalid regex", f)
    return t


def needs_comparator(f):
    def t(x):
        if not re.match("[<>=]\d+", x):
            raise FilterException("Invalid comparator", f)
        return f(x)
    return t


# Coarse text filters:
@needs_nonempty_string
def starts_filter(arg):
    return lambda x: x.startswith(arg)


@needs_nonempty_string
def ends_filter(arg):
    return lambda x: x.endswith(arg)


@needs_nonempty_string
def contains_filter(arg):
    return lambda x: arg in x


@needs_nonempty_string
@needs_regex
def matches_filter(arg):
    return lambda x: re.compile(arg).match(x)


@needs_comparator
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
        raise FilterException("Invalid input to length filter: " + arg, length_filter)
    return t


# Fine text filters:
@needs_nonempty_string
def after_filter(arg):
    return lambda x: x[x.find(arg) + len(arg):] if arg in x else ''


@needs_nonempty_string
def before_filter(arg):
    return lambda x: x[:x.find(arg)] if arg in x else x


@needs_number
def afterpos_filter(arg):
    return lambda x: x[int(arg):]


@needs_number
def beforepos_filter(arg):
    return lambda x: x[:int(arg)]


@needs_nonempty_string
def exclude_filter(arg):
    return lambda x: x.replace(arg, '')


@needs_nonempty_string
def striptags_filter(arg):  # TODO: Improve validation for this.
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


@needs_nonempty_string
def children_filter(arg):  # TODO: Improve validation for this.
    f = _match_tag(arg)
    f.recursive = False
    return f


@needs_nonempty_string
def findall_filter(arg):  # TODO: Improve validation for this.
    f = _match_tag(arg)
    f.recursive = True
    return f


# Fine HTML filters:
@needs_empty_string
def text_filter(_):
    return lambda x: x.getText()


@needs_empty_string
def rawtext_filter(_):
    return lambda x: str(x)


@needs_nonempty_string
def attr_filter(arg):
    def f(x):
        try:
            return x[arg]
        except KeyError:
            return ""
    return f
