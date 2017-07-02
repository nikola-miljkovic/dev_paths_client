from github_browser import cmd_parser
from github_browser.application_context import ListApplicationContext, LatestApplicationContext

import unittest


class CmdParserTests(unittest.TestCase):
    def test_list_default(self):
        application_context = cmd_parser.parse(['list'])

        self.assertIsInstance(application_context, ListApplicationContext)

    def test_list_argument(self):
        application_context = cmd_parser.parse(['list', 'ruby'])

        self.assertIsInstance(application_context, ListApplicationContext)
        self.assertEqual(application_context.selected_language, "ruby")

    def test_list_argument_n(self):
        application_context = cmd_parser.parse(['list','-n', '10'])

        self.assertIsInstance(application_context, ListApplicationContext)
        self.assertEqual(application_context.entry_number, 10)

    def test_list_sort_correct(self):
        application_context = cmd_parser.parse(['list', '-n', '10', '-s', 'stars'])

        self.assertIsInstance(application_context, ListApplicationContext)
        self.assertEqual(application_context.sort_type, 'stars')

    def test_list_sort_wrong(self):
        application_context = cmd_parser.parse(['list', '-n', '10', '-s', 'random'])

        self.assertIsNone(application_context)

    def test_desc_without_arguments(self):
        application_context = cmd_parser.parse(['desc'])

        self.assertIsNone(application_context)

    def test_desc_with_arguments(self):
        application_context = cmd_parser.parse(['desc', 'mojombo/grit', 'mojombo/god'])

        self.assertCountEqual(application_context._search_ids, ['mojombo/grit', 'mojombo/god'])

    def test_latest_without_arguments(self):
        application_context = cmd_parser.parse(['latest'])

        self.assertIsInstance(application_context, LatestApplicationContext)

    def test_no_cmd(self):
        application_context = cmd_parser.parse([])

        self.assertIsNone(application_context)



if __name__ == '__main__':
    unittest.main()
