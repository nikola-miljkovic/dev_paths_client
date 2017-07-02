import unittest
from unittest import mock

from github_browser.application_context.latest_application_context import LatestApplicationContext
from github_browser.test import mocked_requests_get


class LatestApplicationContextTest(unittest.TestCase):
    #
    # get_latest_public_repository()
    #
    @mock.patch('ghtool.application_context.list_application_context.requests.get',
                side_effect=mocked_requests_get)
    def test_get_latest_public_repository(self, mock_get):
        list_application_context = LatestApplicationContext()
        latest_repository = list_application_context.get_latest_public_repository()

        self.assertEqual(latest_repository['id'], 96029576)

if __name__ == '__main__':
    unittest.main()
