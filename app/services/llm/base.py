from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    def generate_remediation(self, context: str) -> str:
        raise NotImplementedError
