#!/usr/bin/python
import sys
import fetchinterpreter
import fetchparser

def interpret(filename):
    try:
        compiled = fetchparser.parse_input(open(filename).read())
    except fetchparser.ParserError as e:
        print "Error parsing input file:", e.msg
        sys.exit(1)
    try:
        for line in compiled:
            fetchinterpreter.handle_line(line)
    except fetchinterpreter.InterpreterException as e:
        print "Error fetching data:", e.msg
        sys.exit(1)
    try:
        print fetchinterpreter.get_output()
    except fetchinterpreter.InterpreterException as e:
        print "Error emitting output:", e.msg
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        print "Fetch needs a filename as an argument."
        sys.exit(1)
    interpret(filename)
