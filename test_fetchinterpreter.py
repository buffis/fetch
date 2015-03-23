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

    def test_filter_matches(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.TextWrapper([
            "HELLO100B",
            "YO100A",
            "hello100b",
            "foobar"
        ])
        action = CoarseFilterAction("x", BasicFilterExpression("matches","[A-Z]+100[ABC]"), "y")
        fetchinterpreter.coarsefilteraction(action)
        output = fetchinterpreter.VARS["x"].output()
        self.assertEquals(2, len(output))
        self.assertTrue("HELLO100B" in output)
        self.assertTrue("YO100A" in output)

    def test_filter_length_gt(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.TextWrapper([
            "hello world",
            "world hello",
            "hello hello",
            "world"
        ])
        action = CoarseFilterAction("x", BasicFilterExpression("length",">5"), "y")
        fetchinterpreter.coarsefilteraction(action)
        output = fetchinterpreter.VARS["x"].output()
        self.assertEquals(3, len(output))
        self.assertTrue("hello world" in output)
        self.assertTrue("world hello" in output)
        self.assertTrue("hello hello" in output)

    def test_filter_length_lt(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.TextWrapper([
            "hello world",
            "world hello",
            "hello hello",
            "world"
        ])
        action = CoarseFilterAction("x", BasicFilterExpression("length","<6"), "y")
        fetchinterpreter.coarsefilteraction(action)
        output = fetchinterpreter.VARS["x"].output()
        self.assertEquals(1, len(output))
        self.assertTrue("world" in output)

    def test_filter_length_eq(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.TextWrapper([
            "hello world",
            "world hello",
            "hello hello",
            "world"
        ])
        action = CoarseFilterAction("x", BasicFilterExpression("length","=5"), "y")
        fetchinterpreter.coarsefilteraction(action)
        output = fetchinterpreter.VARS["x"].output()
        self.assertEquals(1, len(output))
        self.assertTrue("world" in output)

    # Fine filters below.

    def test_filter_after(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.TextWrapper([
            "hello world",
            "world hello",
            "hello hello",
            "world"
        ])
        action = FineFilterAction("x", BasicFilterExpression("after","hell"), "y")
        fetchinterpreter.finefilteraction(action)
        output = fetchinterpreter.VARS["x"].output()
        self.assertEquals(4, len(output))
        self.assertEquals(["o world", "o", "o hello", ""], output)

    def test_filter_before(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.TextWrapper([
            "hello world",
            "world hello",
            "hello hello",
            "world"
        ])
        action = FineFilterAction("x", BasicFilterExpression("before","orl"), "y")
        fetchinterpreter.finefilteraction(action)
        output = fetchinterpreter.VARS["x"].output()
        self.assertEquals(4, len(output))
        self.assertEquals(["hello w", "w", "hello hello", "w"], output)

    def test_filter_afterpos(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.TextWrapper([
            "hello world",
            "world hello",
            "hello hello",
            "world"
        ])
        action = FineFilterAction("x", BasicFilterExpression("afterpos","3"), "y")
        fetchinterpreter.finefilteraction(action)
        output = fetchinterpreter.VARS["x"].output()
        self.assertEquals(4, len(output))
        self.assertEquals(["lo world", "ld hello", "lo hello", "ld"], output)

    def test_filter_beforepos(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.TextWrapper([
            "hello world",
            "world hello",
            "hello hello",
            "world"
        ])
        action = FineFilterAction("x", BasicFilterExpression("beforepos","3"), "y")
        fetchinterpreter.finefilteraction(action)
        output = fetchinterpreter.VARS["x"].output()
        self.assertEquals(4, len(output))
        self.assertEquals(["hel", "wor", "hel", "wor"], output)

    def test_filter_exclude(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.TextWrapper([
            "hello world",
            "world hello",
            "hello hello",
            "world",
            "world world"
        ])
        action = FineFilterAction("x", BasicFilterExpression("exclude","world"), "y")
        fetchinterpreter.finefilteraction(action)
        output = fetchinterpreter.VARS["x"].output()
        self.assertEquals(5, len(output))
        self.assertEquals(["hello ", " hello", "hello hello", "", " "], output)

if __name__ == '__main__':
    unittest.main()