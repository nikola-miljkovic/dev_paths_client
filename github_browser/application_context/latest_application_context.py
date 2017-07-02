import requests

from typing import Dict
from github_browser.application_context import ApplicationContext


class LatestApplicationContext(ApplicationContext):
    PATH_EVENTS = '/events'

    def __init__(self):
        self._latest_repository = None

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
        request_url = ''.join([ApplicationContext.ROOT_ENDPOINT, self.PATH_EVENTS])
        while True:
            request = requests.get(request_url)
            items = request.json()
            entry = next(filter(LatestApplicationContext.is_repository_creation_event, items), None)
            if entry is None:
                try:
                    # Continue to traverse events until we find correct one
                    request_url = request.links['next']['url']
                    continue
                except KeyError:
                    return False
            return entry['repo']

    def get_sanitized_data(self) -> str:
        if self._latest_repository is None:
            return None
        else:
            return self._latest_repository['name']

    def run(self):
        self._latest_repository = self.get_latest_public_repository()
