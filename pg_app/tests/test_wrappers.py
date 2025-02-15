from django.test import TestCase
from pg_app.utils.wrappers.leetcode.leetcode_wrapper import LeetcodeWrapper
from pg_app.utils.wrappers.abstract_wrapper import AbstractRequestWrapper
import asyncio

class AbstractWrapperTestCase(TestCase):
    def setUp(self):
        pass

class LeetcodeTestCase(TestCase):
    def setUp(self):
        self.lw = LeetcodeWrapper()
        
    def test_get_question(self):
        #TODO: Write test cases