import requests
import json

from . import ApplicationContext


class ListApplicationContext(ApplicationContext):
    PATH = '/search/repositories'

    def __init__(self, n: int, lang: str=None, sort: str='updated'):
        self.entry_number = n
        self.selected_language = lang
        self.sort_type = sort

    def get_query_str(self) -> str:
        query_build_str = []
        if self.selected_language is not None:
            query_build_str.append('q=language:%s' % self.selected_language)

        query_build_str.append('per_page=%s' % self.entry_number)
        query_build_str.append('sort=%s' % self.sort_type)
        return '?' + '&'.join(query_build_str)

    def sanatize_data(self, request_dict: dict) -> str:
        pass

    def run(self):
        request_url = ''.join([ApplicationContext.ROOT_ENDPOINT, self.PATH, self.get_query_str()])
        request = requests.get(request_url)

        return self.sanatize_data(request.json())