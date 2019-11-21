"""Describes the output formatter interface."""
import abc
from typing import List


class IOutputFormatter(abc.ABC):
    """Interface to implement for formatting result data into writeable file output."""

    @abc.abstractmethod
    def write_results(self, result_list: List[str]) -> bytes:
        """Convert arbitrary result data into the correct format as writeable bytes."""
        raise NotImplementedError
