from . import ApplicationContext


class ListApplicationContext(ApplicationContext):

    def __init__(self, lang, n):
        self.entry_number = n
        self.selected_language = lang

    def run(self):
        pass