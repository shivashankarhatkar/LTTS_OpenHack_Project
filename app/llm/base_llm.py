"""
Base LLM interface.

Defines the common interface for all Large Language Model providers.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class BaseLLM(ABC):
    """
    Abstract base class for LLM providers.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.2,
    ) -> str:
        """
        Generate a response from the LLM.

        Args:
            prompt:
                Input prompt.

            temperature:
                Sampling temperature.

        Returns:
            Generated text.
        """
        raise NotImplementedError