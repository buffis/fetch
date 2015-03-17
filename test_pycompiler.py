import pycompiler
import unittest
import re

class TestFunctions(unittest.TestCase):
    def setUp(self):
        pass

    def verify_true_filter(self, code, indata):
        self.assertTrue(eval("lambda x:" + code)(indata))
    def verify_false_filter(self, code, indata):
        self.assertFalse(eval("lambda x:" + code)(indata))

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

if __name__ == '__main__':
    unittest.main()
