from abc import ABC, abstractmethod

class LLMInterface(ABC):
    @abstractmethod
    def chat(self, messages, response_format):
        pass
