import unittest

from github_browser.application_context import ListApplicationContext


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

if __name__ == '__main__':
    unittest.main()
