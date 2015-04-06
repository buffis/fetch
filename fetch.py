import fetchparser

def print_parsed():
    for line in fetchparser.parse_input(open("sample.fetch").read()):
        print line

def print_lexed():
    import fetchlexer
    l=fetchlexer.get_lexer()

    # Give the lexer some input
    l.input(open("sample.fetch").read())

    # Tokenize
    while True:
        tok = l.token()
        if not tok: break      # No more input
        print tok

def interpret():
    import fetchinterpreter
    compiled = fetchparser.parse_input(open("sample.fetch").read())
    for line in compiled:
        fetchinterpreter.handle_line(line)
    print "Output", fetchinterpreter.get_output()

def execute_compiled():
    execfile("fetchout.py")

if __name__ == "__main__":
    print "\n--Lexed--"
    print_lexed()

    print "\n--Parsed--"
    try:
        print_parsed()
    except SyntaxError:
        print "Terminating"
        import sys
        sys.exit(1)

    print "\n--Interpreting--"
    interpret()
