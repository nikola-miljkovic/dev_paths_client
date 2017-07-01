from abc import ABC, abstractmethod

class ApplicationContext(ABC):
    ROOT_ENDPOINT = 'https://api.github.com'

    @abstractmethod
    def run(self):
        pass