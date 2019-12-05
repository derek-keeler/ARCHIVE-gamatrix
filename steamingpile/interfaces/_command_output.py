"""Module describing the contract for output objects."""
from typing import IO, List
from steamingpile import types


class ICommandOutput:
    @property
    def information(self) -> List[types.SteamingPileInfo]:
        raise NotImplementedError

    @information.setter
    def information(self, value: List[types.SteamingPileInfo]):
        raise NotImplementedError

    def write(self, stream: IO[str]):
        raise NotImplementedError

