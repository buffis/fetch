#!/usr/bin/python
from fetchutils import *
from fetchfilters import FilterException
import sys
import fetchinterpreter
import fetchparser


def interpret(filename):
    try:
        compiled = fetchparser.parse_input(open(filename).read())
    except fetchparser.ParserError as e:
        exit_with_error("Error parsing input file: %s" % e.msg)

    try:
        for line in compiled:
            fetchinterpreter.handle_line(line)
    except fetchinterpreter.InterpreterException as e:
        exit_with_error("Error fetching data: %s" % e.msg)
    except FilterException as e:
        exit_with_error("Error when filtering data: %s" % e.msg)

    try:
        log(fetchinterpreter.get_output())
    except fetchinterpreter.InterpreterException as e:
        exit_with_error("Error emitting output: %s" % e.msg)


if __name__ == "__main__":
    # TODO: Allow flag for changing mode. Make parsing args better.
    if len(sys.argv) == 2:
        interpret(sys.argv[1])
    else:
        exit_with_error("Fetch needs a single filename as an argument.")
