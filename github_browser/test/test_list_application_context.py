import unittest
from unittest import mock

from github_browser.application_context import ListApplicationContext
from github_browser.test import mocked_requests_get, mocked_get_query_str


class ListApplicationContextTest(unittest.TestCase):

    #
    # get_query_str() tests
    #
    def test_get_query_str_with_all_parameters(self):
        list_application_context = ListApplicationContext(45, lang='ruby')

        query = list_application_context.get_query_str()
        self.assertRegexpMatches(query, r'\?q=created\:.*language:ruby&per_page=100&sort=updated')

    def test_get_query_str_without_language(self):
        list_application_context = ListApplicationContext(45)

        query = list_application_context.get_query_str()
        self.assertRegexpMatches(query, r'\?q=created\:.*&per_page=100&sort=updated')

    def test_get_query_str_with_stars_sort(self):
        list_application_context = ListApplicationContext(45, sort='stars')

        query = list_application_context.get_query_str()
        self.assertRegexpMatches(query, r'\?q=created\:.*&per_page=100&sort=stars')

    #
    # get_sanitized_data()
    #
    @mock.patch('github_browser.application_context.list_application_context.requests.get',
                side_effect=mocked_requests_get)
    @mock.patch('github_browser.application_context.list_application_context.ListApplicationContext.get_query_str',
                side_effect=mocked_get_query_str)
    def test_get_sanitized_data_format(self, mock_get, mock_query):
        expected_format = "Total entries found: 1\n" \
                          "----------------------------------------\n" \
                          "WelshSean/NAND2Tetris"

        list_application_context = ListApplicationContext(1, lang='assembly', sort='updated')
        list_application_context.run()

        self.assertEqual(expected_format, list_application_context.get_sanitized_data())

    #
    # sort_by_creation_date()
    #
    def test_sort_by_creation_date(self):
        time_low, time_high = ListApplicationContext.get_time_range(60)
        time_lowest, _ = ListApplicationContext.get_time_range(120)

        entries = [{'created_at': time_low}, {'created_at': time_high}, {'created_at': time_lowest}]
        new_entries = sorted(entries, key=ListApplicationContext.sort_by_creation_date, reverse=True)
        self.assertListEqual(new_entries,
                             [{'created_at': time_high}, {'created_at': time_low}, {'created_at': time_lowest}])

if __name__ == '__main__':
    unittest.main()
