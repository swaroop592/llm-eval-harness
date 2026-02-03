from abc import ABC, abstractmethod
from typing import Dict

class LLMProvider(ABC):
    """
    Abstract interface for LLM providers.
    """

    @abstractmethod
    def generate(self, prompt: str) -> Dict:
        """
        Returns a dict with:
        - answer (str)
        - evidence (str)
        - confidence (float)
        - latency_ms (float)
        - prompt_tokens (int)
        - completion_tokens (int)
        """
        pass
