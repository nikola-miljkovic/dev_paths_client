import json


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    endpoints = {
        'https://api.github.com/search/repositories?q=language:assembly&per_page=1&sort=updated': 'data/test_data_get_sanatized_data.json',
        'https://api.github.com/events': 'data/test_data_get_latest_repository.json'
    }

    try:
        with open(endpoints[args[0]]) as data_test_file:
            return MockResponse(json.load(data_test_file), 200)
    except KeyError:
        return MockResponse(None, 404)
