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
        self.assertEqual(applicationContext.SelectedLanguage, "ruby")

    def test_list_argument_n(self):
        applicationContext = cmd_parser.parse(['list','-n', '10'])

        self.assertIsInstance(applicationContext, ListApplicationContext)
        self.assertEqual(applicationContext.EntryNumber, 10)

    def test_desc(self):
        applicationContext = cmd_parser.parse(['desc'])

        self.assertIsInstance(applicationContext, DescApplicationContext)

    def test_descargument_n(self):
        applicationContext = cmd_parser.parse(['desc', '-n', '10'])

        self.assertIsInstance(applicationContext, DescApplicationContext)
        self.assertEqual(applicationContext.EntryNumber, 10)

    def test_no_cmd(self):
        applicationContext = cmd_parser.parse([])

        self.assertIsNone(applicationContext)

if __name__ == '__main__':
    unittest.main()
