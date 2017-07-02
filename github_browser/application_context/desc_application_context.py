import asyncio
import concurrent
from typing import List, Generator

import requests

from . import ApplicationContext


class DescApplicationContext(ApplicationContext):
    PATH = '/repos/'

    def __init__(self, ids: List[str]):
        self._search_ids = ids
        self._finished_requests = False
        self._async_requests = None
        self._output_str = None
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

    def run(self):
        loop = asyncio.get_event_loop()
        request_urls = (''.join([ApplicationContext.ROOT_ENDPOINT, self.PATH, id]) for id in self._search_ids)

        total_search_size = len(self._search_ids)
        worker_count = total_search_size if total_search_size < 4 else 5
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=worker_count)
        self._async_requests = (self._executor.submit(requests.get, url) for url in request_urls)

    def get_data_stream(self) -> Generator[str, str, str]:
        if not self._finished_requests and self._async_requests is None:
            return ""
        elif not self._finished_requests:
            self._output_str = ""
            for request in concurrent.futures.as_completed(self._async_requests):
                item = request.result().json()

                entry_output_buffer = list()
                entry_output_buffer.append("----------------------------------------")
                entry_output_buffer.append("Repository Name: %s" % item['full_name'])
                entry_output_buffer.append("Owner: %s" % item['owner']['login'])
                entry_output_buffer.append("Description: \"%s\"" % item['description'])

                new_entry_str = '\n'.join(entry_output_buffer)
                self._output_str = '\n'.join([self._output_str, new_entry_str])

                yield new_entry_str

            self._finished_requests = True
            self._async_requests = None
        else:
            return self._output_str
