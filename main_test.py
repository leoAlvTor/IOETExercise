import unittest
from main import *


class MyFirstTests(unittest.TestCase):

    def test_hello(self):
        self.assertEqual(leo(), 'hello world')
