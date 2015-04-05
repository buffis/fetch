import fetchinterpreter
import fetchparser
import unittest
from requesthandler import TestRequestHandler

class TestFunctions(unittest.TestCase):
    def setUp(self):
        print "Testing: ", self
        fetchinterpreter.VARS = {} # Clean up interpreter state.

    def test_fetch_filterlines_output(self):
        return_data = """Data from a API
This is the line I want to fetch.
I don't want this,
or this."""
        fetch_data = """other <- 'http://www.coolapi.com/getstuff'
x = [contains:'line I want'] other
output = x
"""
        fetchinterpreter.inject_requesthandler_for_test(TestRequestHandler(return_data))
        data = fetchparser.parse_input(fetch_data)
        for line in data:
            fetchinterpreter.handle_line(line)
        output = fetchinterpreter.get_output().output()
        self.assertEquals(["This is the line I want to fetch."], output)

