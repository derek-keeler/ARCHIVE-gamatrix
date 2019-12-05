"""Module describing the contract for output objects."""
from typing import List


class ICommandOutput:
    """Interface describing the command output contract."""

    def append_line_data(self, key: str, values: List[str]):
        raise NotImplementedError

    def write_all(self) -> bytes:
        raise NotImplementedError
