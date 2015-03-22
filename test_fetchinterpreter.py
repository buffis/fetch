import fetchinterpreter
import unittest
from parseractions import *

TEST_URL = "http://stackoverflow.com/questions/8221296/how-can-i-download-and-read-a-url-with-universal-newlines"

class TestFunctions(unittest.TestCase):

    def setUp(self):
        print "Testing: ", self
        fetchinterpreter.VARS = {}

    def test_fetchaction_get(self):
        name = "test"
        action = FetchAction(name, "GET", TEST_URL)
        fetchinterpreter.fetchaction(action)
        self.assertEquals("GET", fetchinterpreter.VARS[name].method)
        self.assertEquals(TEST_URL, fetchinterpreter.VARS[name].url, TEST_URL)

    def test_fetchaction_post(self):
        name = "test"
        action = FetchAction(name, "POST", TEST_URL)
        fetchinterpreter.fetchaction(action)
        self.assertEquals("POST", fetchinterpreter.VARS[name].method)
        self.assertEquals(TEST_URL, fetchinterpreter.VARS[name].url, TEST_URL)

    def test_filter_starts(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.TextWrapper([
            "hello world",
            "world hello",
            "hello hello",
            "world"
        ])
        action = CoarseFilterAction("x", BasicFilterExpression("starts","hello"), "y")
        fetchinterpreter.coarsefilteraction(action)
        output = fetchinterpreter.VARS["x"].output()
        self.assertEquals(2, len(output))
        self.assertTrue("hello world" in output)
        self.assertTrue("hello hello" in output)

    def test_filter_ends(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.TextWrapper([
            "hello world",
            "world hello",
            "hello hello",
            "world"
        ])
        action = CoarseFilterAction("x", BasicFilterExpression("ends","hello"), "y")
        fetchinterpreter.coarsefilteraction(action)
        output = fetchinterpreter.VARS["x"].output()
        self.assertEquals(2, len(output))
        self.assertTrue("world hello" in output)
        self.assertTrue("hello hello" in output)


    def test_filter_contains(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.TextWrapper([
            "hello world",
            "world hello",
            "hello hello",
            "world"
        ])
        action = CoarseFilterAction("x", BasicFilterExpression("contains","d he"), "y")
        fetchinterpreter.coarsefilteraction(action)
        output = fetchinterpreter.VARS["x"].output()
        self.assertEquals(1, len(output))
        self.assertTrue("world hello" in output)


if __name__ == '__main__':
    unittest.main()