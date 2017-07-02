import unittest
from unittest import mock

from github_browser.application_context import ListApplicationContext
from github_browser.test import mocked_requests_get


class ListApplicationContextTest(unittest.TestCase):

    #
    # get_query_str() tests
    #

    def test_get_query_str_with_all_parameters(self):
        listApplicationContext = ListApplicationContext(45, lang='ruby')

        query = listApplicationContext.get_query_str()
        self.assertEqual(query, '?q=language:ruby&per_page=45&sort=updated')

    def test_get_query_str_without_language(self):
        listApplicationContext = ListApplicationContext(45)

        query = listApplicationContext.get_query_str()
        self.assertEqual(query, '?per_page=45&sort=updated')

    def test_get_query_str_with_stars_sort(self):
        listApplicationContext = ListApplicationContext(45, sort='stars')

        query = listApplicationContext.get_query_str()
        self.assertEqual(query, '?per_page=45&sort=stars')

    #
    # get_sanatized_data()
    #

    @mock.patch('github_browser.application_context.list_application_context.requests.get', side_effect=mocked_requests_get)
    def test_get_sanatized_data_format(self, mock_get):
        expected_format = "Total entries found: 1\n" \
                          "----------------------------------------\n" \
                          "Repository Name: WelshSean/NAND2Tetris\n" \
                          "Owner: WelshSean\n" \
                          "Description: \"This repo contains my attempt at the Nand2Tetris course - http://nand2tetris.org/\"\n" \
                          "Created at: 05.06.2017"

        listApplicationContext = ListApplicationContext(1, lang='assembly', sort='updated')
        listApplicationContext.run()

        self.assertEqual(expected_format, listApplicationContext.get_sanatized_data())

if __name__ == '__main__':
    unittest.main()
