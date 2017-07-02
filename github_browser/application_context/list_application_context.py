import datetime

import requests

from typing import Dict
from . import ApplicationContext


class ListApplicationContext(ApplicationContext):
    PATH_SEARCH = '/search/repositories'
    PATH_EVENTS = '/events'

    def __init__(self, n: int, lang: str=None, sort: str='updated'):
        self.entry_number = n
        self.selected_language = lang
        self.sort_type = sort
        self._context_data = None
        self._context_data_sanatized = None

    @staticmethod
    def get_time_range(minutes_diff=60) -> (str, str):
        time_higher = datetime.datetime.now(datetime.timezone.utc)
        time_lower = time_higher - datetime.timedelta(minutes=minutes_diff)
        time_format = "%Y-%m-%dT%H:%M:%SZ"
        return time_lower.strftime(time_format), time_higher.strftime(time_format)

    def get_query_str(self) -> str:
        query_build_str = []

        time_lower, time_higher = ListApplicationContext.get_time_range()
        language_query = "" if self.selected_language is None else ("+language:" + self.selected_language)
        query_build_str.append('q=created:\"%s+..+%s\"%s' % (
            time_lower, time_higher, language_query))
        query_build_str.append('per_page=%s' % self.entry_number)
        query_build_str.append('sort=%s' % self.sort_type)
        return '?' + '&'.join(query_build_str)

    def get_sanitized_data(self) -> str:
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

            self._context_data_sanatized = '\n'.join(response)
            return self._context_data_sanatized

    def run(self):
        request_url = ''.join([ApplicationContext.ROOT_ENDPOINT, self.PATH_SEARCH, self.get_query_str()])
        request = requests.get(request_url)
        a = request.links['next']['url']
        self._context_data = request.json()
