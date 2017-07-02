import datetime

import requests
import json

from . import ApplicationContext


class ListApplicationContext(ApplicationContext):
    PATH = '/search/repositories'

    def __init__(self, n: int, lang: str=None, sort: str='updated'):
        self.entry_number = n
        self.selected_language = lang
        self.sort_type = sort
        self._context_data = None
        self._context_data_sanatized = None

    def get_query_str(self) -> str:
        query_build_str = []
        if self.selected_language is not None:
            query_build_str.append('q=language:%s' % self.selected_language)

        query_build_str.append('per_page=%s' % self.entry_number)
        query_build_str.append('sort=%s' % self.sort_type)
        return '?' + '&'.join(query_build_str)

    def get_sanatized_data(self) -> str:
        if self._context_data_sanatized is not None:
            return self._context_data_sanatized
        elif self._context_data is None:
            return ""
        else:
            response = list()
            items = self._context_data['items']
            response.append("Total entries found: %s" % len(items))

            for item in items:
                response.append("----------------------------------------")
                response.append("Repository Name: %s" % item['full_name'])
                response.append("Owner: %s" % item['owner']['login'])
                response.append("Description: \"%s\"" % item['description'])
                response.append("Created at: %s" % datetime.datetime.strptime(item['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                                .strftime("%m.%d.%Y"))

            self._context_data_sanatized = '\n'.join(response)
            return self._context_data_sanatized

    def run(self):
        request_url = ''.join([ApplicationContext.ROOT_ENDPOINT, self.PATH, self.get_query_str()])
        request = requests.get(request_url)
        self._context_data = request.json()
