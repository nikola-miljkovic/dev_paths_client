import asyncio
import concurrent
from typing import List, Generator

import requests

from . import ApplicationContext


class DescApplicationContext(ApplicationContext):
    PATH = '/repos/'

    def __init__(self, ids: List[str]):
        self._search_ids = ids
        self._async_requests = None
        self._sanitized_data = None
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

    def run(self):
        loop = asyncio.get_event_loop()
        request_urls = (''.join([ApplicationContext.ROOT_ENDPOINT, self.PATH, id]) for id in self._search_ids)

        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
        self._async_requests = (self._executor.submit(requests.get, url) for url in request_urls)

    def get_data_stream(self) -> Generator[str, str, str]:
        if self._async_requests is None:
            return ""

        self._sanitized_data = ""
        for request in concurrent.futures.as_completed(self._async_requests):
            item = request.result().json()

            new_entry = list()
            new_entry.append("----------------------------------------")
            new_entry.append("Repository Name: %s" % item['full_name'])
            new_entry.append("Owner: %s" % item['owner']['login'])
            new_entry.append("Description: \"%s\"" % item['description'])

            new_entry_str = '\n'.join(new_entry)
            '\n'.join([self._sanitized_data, new_entry_str])

            yield new_entry_str

        return self._sanitized_data
