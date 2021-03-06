import fetchinterpreter
import unittest
from parseractions import *
from BeautifulSoup import BeautifulSoup

TEST_URL = "http://example.com/cool_api"


class TestFunctions(unittest.TestCase):
    def setUp(self):
        print "Testing: ", self
        fetchinterpreter.VARS = {}

    def test_fetchaction_get(self):
        name = "test"
        action = FetchAction(name, "GET", TEST_URL)
        fetchinterpreter.handle_line(action)
        self.assertEquals("GET", fetchinterpreter.VARS[name].method)
        self.assertEquals(TEST_URL, fetchinterpreter.VARS[name].url, TEST_URL)

    def test_fetchaction_post(self):
        name = "test"
        action = FetchAction(name, "POST", TEST_URL)
        fetchinterpreter.handle_line(action)
        self.assertEquals("POST", fetchinterpreter.VARS[name].method)
        self.assertEquals(TEST_URL, fetchinterpreter.VARS[name].url, TEST_URL)

    def test_filter_starts(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.TextWrapper([
            "hello world",
            "world hello",
            "hello hello",
            "world"
        ])
        action = CoarseFilterAction("x", BasicFilterExpression("starts", "hello"), "y")
        fetchinterpreter.handle_line(action)
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
        action = CoarseFilterAction("x", BasicFilterExpression("ends", "hello"), "y")
        fetchinterpreter.handle_line(action)
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
        fetchinterpreter.handle_line(action)
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
        fetchinterpreter.handle_line(action)
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
        fetchinterpreter.handle_line(action)
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
        fetchinterpreter.handle_line(action)
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
        fetchinterpreter.handle_line(action)
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
        fetchinterpreter.handle_line(action)
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
        fetchinterpreter.handle_line(action)
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
        fetchinterpreter.handle_line(action)
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
        fetchinterpreter.handle_line(action)
        output = fetchinterpreter.VARS["x"].output()
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
        fetchinterpreter.handle_line(action)
        output = fetchinterpreter.VARS["x"].output()
        self.assertEquals(["hello ", " hello", "hello hello", "", " "], output)

    def test_filter_striptags_img(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.TextWrapper([
            "hello <p>foobar</p> world",
            "hello <img src='pic.jpg'/> world",
            "hello <img src='pic.jpg'/><img src='pic.jpg'/> world",
            "hello <p>hello</p><img src='pic.jpg'/>world",
        ])
        action = FineFilterAction("x", BasicFilterExpression("striptags","img"), "y")
        fetchinterpreter.handle_line(action)
        output = fetchinterpreter.VARS["x"].output()
        self.assertEquals([
            "hello <p>foobar</p> world",
            "hello  world",
            "hello  world",
            "hello <p>hello</p>world"], output)

    def test_filter_striptags_p_and_img(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.TextWrapper([
            "hello <p>foobar</p> world",
            "hello <img src='pic.jpg'/> world",
            "hello <img src='pic.jpg'/><img src='pic.jpg'/> world",
            "hello <p>hello</p><img src='pic.jpg'/>world",
        ])
        action = FineFilterAction("x", BasicFilterExpression("striptags","p,img"), "y")
        fetchinterpreter.handle_line(action)
        output = fetchinterpreter.VARS["x"].output()
        self.assertEquals([
            "hello  world",
            "hello  world",
            "hello  world",
            "hello world"], output)

    def test_filter_html_children(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.HtmlWrapper(
            [BeautifulSoup("<html><head><title>Page title</title></head></html>")])
        action = CoarseFilterAction("x", BasicFilterExpression("children","html"), "y")
        fetchinterpreter.handle_line(action)
        action = FineFilterAction("x", BasicFilterExpression("rawtext",""), "x")
        fetchinterpreter.handle_line(action)
        output = fetchinterpreter.VARS["x"].output()
        self.assertEquals(
            ["<html><head><title>Page title</title></head></html>"], output)

    def test_filter_html_children_with_class(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.HtmlWrapper(
            [BeautifulSoup("<p class='a'>p1</p><p class='a'>p2</p><p>p3</p>")])
        action = CoarseFilterAction("x", BasicFilterExpression("children","p.a"), "y")
        fetchinterpreter.handle_line(action)
        action = FineFilterAction("x", BasicFilterExpression("rawtext",""), "x")
        fetchinterpreter.handle_line(action)
        output = fetchinterpreter.VARS["x"].output()
        self.assertEquals(
            ['<p class="a">p1</p>', '<p class="a">p2</p>'], output)

    def test_filter_html_findall_children_with_class_too_deep(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.HtmlWrapper(
            [BeautifulSoup("<html><body><p class='a'>p1</p><p class='b'>p2</p><p>p3</p></body></html>")])
        action = CoarseFilterAction("x", BasicFilterExpression("children","p.a"), "y")
        fetchinterpreter.handle_line(action)
        action = FineFilterAction("x", BasicFilterExpression("rawtext",""), "x")
        fetchinterpreter.handle_line(action)
        output = fetchinterpreter.VARS["x"].output()
        self.assertEquals([], output)

    def test_filter_html_findall_tag(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.HtmlWrapper(
            [BeautifulSoup("<html><body><p>p1</p><p>p2</p><p>p3</p></body></html>")])
        action = CoarseFilterAction("x", BasicFilterExpression("findall","p"), "y")
        fetchinterpreter.handle_line(action)
        action = FineFilterAction("x", BasicFilterExpression("rawtext",""), "x")
        fetchinterpreter.handle_line(action)
        output = fetchinterpreter.VARS["x"].output()
        self.assertEquals(
            ['<p>p1</p>', '<p>p2</p>', '<p>p3</p>'], output)

    def test_filter_html_findall_tag_with_class(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.HtmlWrapper(
            [BeautifulSoup("<html><body><p class='a'>p1</p><p class='b'>p2</p><p>p3</p></body></html>")])
        action = CoarseFilterAction("x", BasicFilterExpression("findall","p.a"), "y")
        fetchinterpreter.handle_line(action)
        action = FineFilterAction("x", BasicFilterExpression("rawtext",""), "x")
        fetchinterpreter.handle_line(action)
        output = fetchinterpreter.VARS["x"].output()
        self.assertEquals(
            ['<p class="a">p1</p>'], output)

    def test_filter_html_attr(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.HtmlWrapper(
            [BeautifulSoup("<html><body><img src='things'/><img srcs='stuff'/></body></html>")])
        action = CoarseFilterAction("x", BasicFilterExpression("findall","img"), "y")
        fetchinterpreter.handle_line(action)
        action = FineFilterAction("x", BasicFilterExpression("attr","src"), "x")
        fetchinterpreter.handle_line(action)
        output = fetchinterpreter.VARS["x"].output()
        self.assertEquals(
            ["things", ""], output)

    def test_neg_coarse_filter(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.TextWrapper([
            "hello world",
            "world hello",
            "hello hello",
            "world"
        ])
        action = CoarseFilterAction("x",
                                    NegFilterExpression(BasicFilterExpression("starts","hello")),
                                    "y")
        fetchinterpreter.handle_line(action)
        output = fetchinterpreter.VARS["x"].output()
        self.assertEquals(["world hello", "world"], output)

    def test_combined_filter_or(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.TextWrapper([
            "hello world",
            "goodbye world",
            "hello hello",
            "world hello",
            "world goodbye"
        ])
        action = CoarseFilterAction("x",
                                    CombinedFilterExpression(
                                        BasicFilterExpression("starts","hello"),
                                        BasicFilterExpression("starts","goodbye"),
                                        "|"
                                    ),
                                    "y")
        fetchinterpreter.handle_line(action)
        output = fetchinterpreter.VARS["x"].output()
        self.assertEquals([
            "hello world",
            "goodbye world",
            "hello hello"
        ], output)

    def test_combined_filter_and(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.TextWrapper([
            "hello world",
            "goodbye world",
            "hello hello",
            "world hello",
            "hello goodbye"
        ])
        action = CoarseFilterAction("x",
                                    CombinedFilterExpression(
                                        BasicFilterExpression("starts","hello"),
                                        BasicFilterExpression("ends","goodbye"),
                                        "&"
                                    ),
                                    "y")
        fetchinterpreter.handle_line(action)
        output = fetchinterpreter.VARS["x"].output()
        self.assertEquals(["hello goodbye"], output)

    def test_combined_filter_and_noresult(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.TextWrapper([
            "hello world",
            "goodbye world",
            "hello hello",
            "world hello",
            "world goodbye"
        ])
        action = CoarseFilterAction("x",
                                    CombinedFilterExpression(
                                        BasicFilterExpression("starts","hello"),
                                        BasicFilterExpression("starts","goodbye"),
                                        "&"
                                    ),
                                    "y")
        fetchinterpreter.handle_line(action)
        output = fetchinterpreter.VARS["x"].output()
        self.assertEquals([], output)

    def test_assignment(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.TextWrapper(["hello world"])
        action = OutputAssignment("x", "y")
        fetchinterpreter.handle_line(action)
        self.assertTrue("x" in fetchinterpreter.VARS)
        self.assertEquals(["hello world"], fetchinterpreter.VARS["x"].output())

    def test_assignment_plus(self):
        fetchinterpreter.VARS["y1"] = fetchinterpreter.TextWrapper(["hello world"])
        fetchinterpreter.VARS["y2"] = fetchinterpreter.TextWrapper(["goodbye world"])
        action = OutputAssignment("x", ListPlus("y1", "y2"))
        fetchinterpreter.handle_line(action)
        self.assertTrue("x" in fetchinterpreter.VARS)
        self.assertEquals(["hello world", "goodbye world"], fetchinterpreter.VARS["x"].output())

    def test_assignment_valueat(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.TextWrapper(["hello", "world", "goodbye"])
        action = OutputAssignment("x", ListAt("y", "1"))
        fetchinterpreter.handle_line(action)
        self.assertTrue("x" in fetchinterpreter.VARS)
        self.assertEquals(["world"], fetchinterpreter.VARS["x"].output())

    def test_assignment_valueat_notinrange(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.TextWrapper(["hello", "world", "goodbye"])
        action = OutputAssignment("x", ListAt("y", "10"))
        try:
            fetchinterpreter.handle_line(action)
            self.fail("Expected failure")
        except fetchinterpreter.InterpreterException:
            pass  # Expected

    def test_assignment_dict(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.TextWrapper(["hello world"])
        action = OutputAssignment("x", {"z": "y"})
        fetchinterpreter.handle_line(action)
        self.assertTrue("x" in fetchinterpreter.VARS)
        self.assertTrue("z" in fetchinterpreter.VARS["x"])
        self.assertEquals(["hello world"], fetchinterpreter.VARS["x"]["z"].output())

    def test_assignment_dict_lvalue(self):
        fetchinterpreter.VARS["y"] = fetchinterpreter.TextWrapper(["hello world"])
        fetchinterpreter.VARS["x"] = {}
        action = OutputAssignment(DictAt("x","z"), "y")
        fetchinterpreter.handle_line(action)
        self.assertEquals(["hello world"], fetchinterpreter.VARS["x"]["z"].output())

if __name__ == '__main__':
    unittest.main()