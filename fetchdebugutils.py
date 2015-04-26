def print_lexed(filename):
    import fetchlexer
    l=fetchlexer.get_lexer()

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
