import json


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'https://api.github.com/search/repositories?q=language:assembly&per_page=1&sort=updated':
        with open('data/test_data_get_sanatized_data.json') as data_test_file:
            return MockResponse(json.load(data_test_file), 200)

    return MockResponse(None, 404)