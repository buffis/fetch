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


print "\n--Lexed--"
print_lexed()
print "\n--Parsed--"
print_parsed()
print "\n--Compiled--"
print_compiled()

