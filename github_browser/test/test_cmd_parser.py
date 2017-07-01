from github_browser import cmd_parser
from github_browser.application_context import ListApplicationContext, DescApplicationContext

import unittest

class CmdParserTests(unittest.TestCase):
    def test_list_default(self):
        applicationContext = cmd_parser.parse(['list'])

        self.assertIsInstance(applicationContext, ListApplicationContext)

    def test_list_argument(self):
        applicationContext = cmd_parser.parse(['list', 'ruby'])

        self.assertIsInstance(applicationContext, ListApplicationContext)
        self.assertEqual(applicationContext.selected_language, "ruby")

    def test_list_argument_n(self):
        applicationContext = cmd_parser.parse(['list','-n', '10'])

        self.assertIsInstance(applicationContext, ListApplicationContext)
        self.assertEqual(applicationContext.entry_number, 10)

    def test_list_sort_correct(self):
        applicationContext = cmd_parser.parse(['list', '-n', '10', '-s', 'stars'])

        self.assertIsInstance(applicationContext, ListApplicationContext)
        self.assertEqual(applicationContext.sort_type, 'stars')

    def test_list_sort_wrong(self):
        applicationContext = cmd_parser.parse(['list', '-n', '10', '-s', 'random'])

        self.assertIsNone(applicationContext)

    def test_desc(self):
        applicationContext = cmd_parser.parse(['desc'])

        self.assertIsInstance(applicationContext, DescApplicationContext)

    def test_desc_argument_n(self):
        applicationContext = cmd_parser.parse(['desc', '-n', '10'])

        self.assertIsInstance(applicationContext, DescApplicationContext)
        self.assertEqual(applicationContext.entry_number, 10)

    def test_no_cmd(self):
        applicationContext = cmd_parser.parse([])

        self.assertIsNone(applicationContext)



if __name__ == '__main__':
    unittest.main()
