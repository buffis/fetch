"""
Stuff that can be used to debug Fetch files and/or the fetch lexer, parser or interpreter.

IMPORTANT: Other modules are _not_ allowed to have dependencies on this one.
"""

def print_lexed(filename):
    import fetchlexer
    l = fetchlexer.get_lexer()

    # Give the lexer some input
    l.input(open(filename).read())

    # Tokenize
    while True:
        tok = l.token()
        if not tok: break      # No more input
        print tok

def print_parsed(filename):
    import fetchparser
    for line in fetchparser.parse_input(open(filename).read()):
        print line

if __name__ == "__main__":
    pass  # TODO: Implement.
else:
    raise RuntimeError("Importing fetchdebugutils from other modules is NOT allowed.")