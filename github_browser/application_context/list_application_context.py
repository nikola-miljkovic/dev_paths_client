import datetime

import requests

from typing import Dict
from . import ApplicationContext


class ListApplicationContext(ApplicationContext):
    PATH = '/search/repositories'
    EVENTS_PATH = '/events'

    def __init__(self, n: int, lang: str=None, sort: str='updated'):
        self.entry_number = n
        self.selected_language = lang
        self.sort_type = sort
        self._context_data = None
        self._context_data_sanatized = None

    @staticmethod
    def is_repository_creation_event(event: Dict) -> bool:
        try:
            if event['type'] == 'CreateEvent' and event['payload']['ref_type'] == 'repository':
                return True

            return False
        except KeyError:
            return False

    def get_latest_public_repository(self) -> Dict:
        """
            Searches throughout events for latest public repository created on github
            Where CreateEvent and ref_type is repository
        """
        request_url = ''.join([ApplicationContext.ROOT_ENDPOINT, self.EVENTS_PATH])
        while True:
            request = requests.get(request_url)
            items = request.json()
            entry = next(filter(ListApplicationContext.is_repository_creation_event, items), None)
            if entry is None:
                try:
                    # Continue to traverse events until we find correct one
                    request_url = request.links['next']['url']
                    continue
                except KeyError:
                    return False
            return entry

    def get_query_str(self) -> str:
        query_build_str = []
        if self.selected_language is not None:
            query_build_str.append('q=language:%s' % self.selected_language)

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
        #latest_repo = self.get_latest_public_repository()
        request_url = ''.join([ApplicationContext.ROOT_ENDPOINT, self.PATH, self.get_query_str()])
        request = requests.get(request_url)
        self._context_data = request.json()
