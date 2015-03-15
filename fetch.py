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

def print_compiled():
    import pycompiler
    compiled = fetchparser.parse_input(open("sample.fetch").read())
    
    data = ""
    data += pycompiler.compile_deps()
    for line in compiled:
        data += pycompiler.compile_line(line)
    data += pycompiler.compile_finish()

    print data
    # Write Python code to a file
    f=open("fetchout.py","w")
    f.write(data)
    f.close()

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
        
    print "\n--Compiled--"
    print_compiled()
    print "\n--Executing--"
    execfile("fetchout.py")
