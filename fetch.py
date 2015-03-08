import lexer

lexer = lexer.get_lexer()
lexer.input(open("reddit.fetch").read())
while 1:
    tok = lexer.token()
    if not tok: break
    print tok
