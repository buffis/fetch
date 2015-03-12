import fetchparser

def print_parsed():
    for line in fetchparser.parse_input(open("reddit.fetch").read()):
        print line

def print_lexed():
    import fetchlexer
    l=fetchlexer.get_lexer()

    # Give the lexer some input
    l.input(open("reddit.fetch").read())

    # Tokenize
    while True:
        tok = l.token()
        if not tok: break      # No more input
        print tok

def print_compiled():
    import pycompiler
    compiled = fetchparser.parse_input(open("reddit.fetch").read())
    pycompiler.compile_deps()

    for line in compiled:
        pycompiler.compile_line(line)



print "\n--Lexed--"
print_lexed()
print "\n--Parsed--"
print_parsed()
print "\n--Compiled--"
print_compiled()

