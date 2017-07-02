from datetime import datetime, timedelta, timezone

import requests

from . import ApplicationContext


class ListApplicationContext(ApplicationContext):
    PATH_SEARCH = '/search/repositories'
    PATH_EVENTS = '/events'

    def __init__(self, n: int, lang: str = None, sort: str = 'default', extended_output=False):
        self.entry_number = n
        self.selected_language = lang
        self.sort_type = sort
        self.extended_output = extended_output
        self._context_data = None
        self._context_data_sanitized = None

    @staticmethod
    def get_time_range(minutes_diff) -> (str, str):
        time_higher = datetime.now(timezone.utc)
        time_lower = time_higher - timedelta(minutes=minutes_diff)
        time_format = "%Y-%m-%dT%H:%M:%SZ"
        return time_lower.strftime(time_format), time_higher.strftime(time_format)

    @staticmethod
    def sort_by_creation_date(item):
        return item['created_at']

    @staticmethod
    def transform_date(date):
        time_format_old = "%Y-%m-%dT%H:%M:%SZ"
        time_format_new = "%d.%m.%Y--%H:%M:%S"
        return datetime.strptime(date, time_format_old).strftime(time_format_new)

    def get_query_str(self, minutes_diff=60) -> str:
        time_lower, time_higher = ListApplicationContext.get_time_range(minutes_diff)
        language_query = "" if self.selected_language is None else ("+language:" + self.selected_language)

        query_build_str = ['q=created:\"%s+..+%s\"%s' % (time_lower, time_higher, language_query)]
        query_build_str.append('per_page=100')

        # If sort type is default then we should query with updated
        # as 'default' is CUSTOM type not supported by Octopus API
        query_build_str.append('sort=%s' % ('updated' if self.sort_type == 'default' else self.sort_type))

        return '?' + '&'.join(query_build_str)

    def get_sanitized_data(self) -> str:
        if self._context_data_sanitized is not None:
            return self._context_data_sanitized
        elif self._context_data is None:
            return ""
        else:
            response = list()
            items = self._context_data
            response.append("Total entries found: %s" % len(items))
            response.append("----------------------------------------")

            if self.extended_output:
                response.append('\n'.join("#%s\t%s\t%s" %
                                          (idx, i['full_name'], ListApplicationContext.transform_date(i['created_at']))
                                          for idx, i in enumerate(items)))
            else:
                response.append('\n'.join(i['full_name'] for i in items))

            self._context_data_sanitized = '\n'.join(response)
            return self._context_data_sanitized

    def run(self):
        time_diff = 30
        request_url = ''.join([ApplicationContext.ROOT_ENDPOINT, self.PATH_SEARCH, self.get_query_str(time_diff)])

        items = []
        if self.sort_type == 'default':
            while True:
                request = requests.get(request_url)
                content = request.json()
                items.extend(content['items'])
                total_count = content['total_count']

                if total_count > self.entry_number:
                    # traverse the list until we have all entries to sort
                    try:
                        request_url = request.links['next']['url']
                        continue
                    except KeyError:
                        break
                elif total_count == self.entry_number:
                    break
                else:
                    # create new query with increased time diff so we can get larger total_count
                    try:
                        if time_diff > 180:
                            # if we didn't find yet increase time diff for 1 year
                            time_diff += 60 * 24 * 365

                        time_diff += 60
                        request_url = ''.join(
                            [ApplicationContext.ROOT_ENDPOINT, self.PATH_SEARCH, self.get_query_str(time_diff)])
                        items = []
                        continue
                    except KeyError:
                        break

            items = sorted(items, key=ListApplicationContext.sort_by_creation_date, reverse=True)

        else:
            request = requests.get(request_url)
            content = request.json()
            items.extend(content['items'])

        # a = request.links['next']['url']

        self._context_data = items[0:self.entry_number]
