import pycompiler
import unittest
import re

# Copied from deps. TODO: Refactor to avoid copy+paste
def striptags(x, v):
    tags = v.split(",")
    subbed = x
    for tag in tags:
        subbed = re.sub(r'<%s.*?>.*?</%s>' % (tag, tag), '', subbed)
        subbed = re.sub(r'<%s.*?/>' % tag, '', subbed)
    return subbed

class TestFunctions(unittest.TestCase):
    def setUp(self):
        pass

    def verify_true_filter(self, code, indata):
        self.assertTrue(eval("lambda x:" + code)(indata))
    def verify_false_filter(self, code, indata):
        self.assertFalse(eval("lambda x:" + code)(indata))
    def verify_fine_filter(self, code, indata, expected_outdata):
        self.assertEquals(expected_outdata, eval("lambda x:" + code)(indata))

    def test_starts_filter(self):
        code = pycompiler.compile_starts_filter("'hel'")
        self.verify_true_filter(code, "hello world")
        self.verify_true_filter(code, "helium")
        self.verify_false_filter(code, "HELLO")
        self.verify_false_filter(code, "foobar")

    def test_ends_filter(self):
        code = pycompiler.compile_ends_filter("'rld'")
        self.verify_true_filter(code, "hello world")
        self.verify_true_filter(code, "world")
        self.verify_false_filter(code, "WORLD")
        self.verify_false_filter(code, "foobar")

    def test_contains_filter(self):
        code = pycompiler.compile_contains_filter("'llo'")
        self.verify_true_filter(code, "hello world")
        self.verify_true_filter(code, "lollollol")
        self.verify_false_filter(code, "HELLO")
        self.verify_false_filter(code, "foobar")        

    def test_length_filter(self):
        code = pycompiler.compile_length_filter("'>5'")
        self.verify_true_filter(code, "hello world")
        self.verify_true_filter(code, "lollollol")
        self.verify_false_filter(code, "HELLO")
        self.verify_false_filter(code, "foo")
        code = pycompiler.compile_length_filter("'<5'")
        self.verify_false_filter(code, "hello world")
        self.verify_false_filter(code, "lollollol")
        self.verify_false_filter(code, "HELLO")
        self.verify_true_filter(code, "foo")
        code = pycompiler.compile_length_filter("'==5'")
        self.verify_false_filter(code, "hello world")
        self.verify_false_filter(code, "lollollol")
        self.verify_true_filter(code, "HELLO")
        self.verify_false_filter(code, "foo")

    def test_matches_filter(self):
        code = pycompiler.compile_matches_filter("'[A-Z]+100[ABC]'")
        self.verify_true_filter(code, "HELLO100B")
        self.verify_true_filter(code, "YO100A")
        self.verify_false_filter(code, "hello100b")
        self.verify_false_filter(code, "foobar")

    def test_after_filter(self):
        code = pycompiler.compile_after_filter("'ello'")
        self.verify_fine_filter(code, "hello world", " world")
        self.verify_fine_filter(code, "hello hi, hello hey", " hi, hello hey")
        self.verify_fine_filter(code, "foobar", "")

    def test_before_filter(self):
        code = pycompiler.compile_before_filter("'llo'")
        self.verify_fine_filter(code, "hello world", "he")
        self.verify_fine_filter(code, "hello hi, hello hey", "he")
        self.verify_fine_filter(code, "foobar", "foobar")

    def test_afterpos_filter(self):
        code = pycompiler.compile_afterpos_filter("'0'")
        self.verify_fine_filter(code, "hello world", "hello world")
        code = pycompiler.compile_afterpos_filter("'2'")
        self.verify_fine_filter(code, "hello world", "llo world")
        code = pycompiler.compile_afterpos_filter("'200'")
        self.verify_fine_filter(code, "hello world", "")

    def test_beforepos_filter(self):
        code = pycompiler.compile_beforepos_filter("'0'")
        self.verify_fine_filter(code, "hello world", "")
        code = pycompiler.compile_beforepos_filter("'2'")
        self.verify_fine_filter(code, "hello world", "he")
        code = pycompiler.compile_beforepos_filter("'200'")
        self.verify_fine_filter(code, "hello world", "hello world")

    def test_exclude_filter(self):
        code = pycompiler.compile_exclude_filter("'lo'")
        self.verify_fine_filter(code, "hello world", "hel world")
        self.verify_fine_filter(code, "hello hello", "hel hel")
        self.verify_fine_filter(code, "foobar", "foobar")

    def test_striptags_filter(self):
        # TODO: Only support one tag currently, fix
        code = pycompiler.compile_striptags_filter("'p'")
        self.verify_fine_filter(code, "hello <p>foobar</p> world", "hello  world")
        code = pycompiler.compile_striptags_filter("'img'")
        self.verify_fine_filter(code,
                                "hello <img src='pic.jpg'/> world",
                                "hello  world")
        self.verify_fine_filter(code,
                                "hello <img src='pic.jpg'/><img src='pic.jpg'/> world",
                                "hello  world")
        code = pycompiler.compile_striptags_filter("'p,img'")
        self.verify_fine_filter(code,
                                "hello <p>hello</p><img src='pic.jpg'/>world",
                                "hello world")

if __name__ == '__main__':
    unittest.main()
