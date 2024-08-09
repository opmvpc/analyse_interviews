from abc import ABC, abstractmethod

class LLMInterface(ABC):
    @abstractmethod
    def json(self, messages, response_format):
        pass
