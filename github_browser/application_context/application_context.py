from abc import ABC, abstractmethod

class ApplicationContext(ABC):
    @abstractmethod
    def run(self):
        pass