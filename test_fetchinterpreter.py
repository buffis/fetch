import fetchinterpreter
import unittest
from parseractions import *

TEST_URL = "http://stackoverflow.com/questions/8221296/how-can-i-download-and-read-a-url-with-universal-newlines"

class TestFunctions(unittest.TestCase):

    def setUp(self):
        pass

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



if __name__ == '__main__':
    unittest.main()