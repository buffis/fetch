#!/usr/bin/python
import sys
import fetchparser

def interpret(filename):
    import fetchinterpreter
    compiled = fetchparser.parse_input(open(filename).read())
    for line in compiled:
        fetchinterpreter.handle_line(line)
    print fetchinterpreter.get_output()

if __name__ == "__main__":
    print "\n--Interpreting--"
    filename = "samples/github_buffis_repoinfo.fetch" # TODO: Remove this default prior to making public
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    interpret(filename)
