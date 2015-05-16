import fetchinterpreter
import fetchparser
import unittest
from requesthandler import TestRequestHandler


class TestFunctions(unittest.TestCase):
    def setUp(self):
        print "Testing: ", self
        fetchinterpreter.VARS = {}  # Clean up interpreter state.

    def test_fetch_filterlines_output(self):
        return_data = """Data from a API
This is the line I want to fetch.
I don't want this,
or this."""
        fetch_data = """other <- 'http://www.coolapi.com/getstuff'
x = [contains:'line I want'|contains:'notpresent'] other
x = {after:' is '} x
y = {exclude: 'e'} x
output = y
"""
        fetchinterpreter.inject_requesthandler_for_test(TestRequestHandler(return_data))
        data = fetchparser.parse_input(fetch_data)
        for line in data:
            fetchinterpreter.handle_line(line)
        output = fetchinterpreter.get_output().output()
        self.assertEquals(["th lin I want to ftch."], output)

    def test_fetch_filter_html_output(self):
        return_data = """<html><head><title>Page title</title></head>
<body><p id="firstpara" align="center">This is paragraph <b>one</b>.
<p id="secondpara" align="blah">This is paragraph <b>two</b>.
</html>"""
        fetch_data = """other <- 'http://www.coolapi.com/getstuff'
x = [children:'html'] other
x = [children:'head'] x
x = [children:'title'] x
y = {text:''} x
output = y
"""
        fetchinterpreter.inject_requesthandler_for_test(TestRequestHandler(return_data))
        data = fetchparser.parse_input(fetch_data)
        for line in data:
            fetchinterpreter.handle_line(line)
        output = fetchinterpreter.get_output().output()
        self.assertEquals(["Page title"], output)
