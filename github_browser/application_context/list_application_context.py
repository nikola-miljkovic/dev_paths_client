from . import ApplicationContext


class ListApplicationContext(ApplicationContext):

    def __init__(self, lang, n):
        self._lang = lang
        self._n = n

    def run(self):
        pass