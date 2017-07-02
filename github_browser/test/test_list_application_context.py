import unittest
from unittest import mock

from github_browser.application_context import ListApplicationContext
from github_browser.test import mocked_requests_get


class ListApplicationContextTest(unittest.TestCase):

    #
    # get_query_str() tests
    #
    def test_get_query_str_with_all_parameters(self):
        list_application_context = ListApplicationContext(45, lang='ruby')

        query = list_application_context.get_query_str()
        self.assertEqual(query, '?q=language:ruby&per_page=45&sort=updated')

    def test_get_query_str_without_language(self):
        list_application_context = ListApplicationContext(45)

        query = list_application_context.get_query_str()
        self.assertEqual(query, '?per_page=45&sort=updated')

    def test_get_query_str_with_stars_sort(self):
        list_application_context = ListApplicationContext(45, sort='stars')

        query = list_application_context.get_query_str()
        self.assertEqual(query, '?per_page=45&sort=stars')

    #
    # get_sanitized_data()
    #
    @mock.patch('github_browser.application_context.list_application_context.requests.get',
                side_effect=mocked_requests_get)
    def test_get_sanitized_data_format(self, mock_get):
        expected_format = "Total entries found: 1\n" \
                          "----------------------------------------\n" \
                          "Repository Name: WelshSean/NAND2Tetris\n" \
                          "Owner: WelshSean\n" \
                          "Description: \"This repo contains my attempt at the Nand2Tetris course - http://nand2tetris.org/\""

        list_application_context = ListApplicationContext(1, lang='assembly', sort='updated')
        list_application_context.run()

        self.assertEqual(expected_format, list_application_context.get_sanitized_data())

    #
    # get_latest_public_repository()
    #
    @mock.patch('github_browser.application_context.list_application_context.requests.get',
                side_effect=mocked_requests_get)
    def test_get_latest_public_repository(self, mock_get):
        list_application_context = ListApplicationContext(1, lang='assembly', sort='updated')
        latest_repository = list_application_context.get_latest_public_repository()

        self.assertEqual(latest_repository['id'], '6178645124')

if __name__ == '__main__':
    unittest.main()
