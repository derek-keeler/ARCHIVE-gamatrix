import abc
import json
import csv
import dataclasses
from typing import IO, List
from steamingpile import types
from steamingpile import interfaces


class ABCOutput(abc.ABC, interfaces.ICommandOutput):
    _info: List[types.SteamingPileInfo] = []

    def __init__(self, initial_data: List[types.SteamingPileInfo] = []):
        d = []
        if initial_data:
            d = initial_data
        self.information = d

    @property
    def information(self) -> List[types.SteamingPileInfo]:
        return self._info

    @information.setter
    def information(self, value: List[types.SteamingPileInfo]):
        self._info = value

    @abc.abstractmethod
    def write(to_stream: IO[str]):
        raise NotImplementedError("All subclasses must implement the write method.")


class BasicOutputter(ABCOutput):
    _info: List[object]

    def __init__(self, initial_data: List[types.SteamingPileInfo] = []):
        super().__init__(initial_data)

    def write(self, stream: IO[str]):
        lines = [f"{inf.__str__()}\n" for inf in self.information]
        stream.writelines(lines)


class TextOutputter(ABCOutput):
    def write(self, stream: IO[str]):
        for inf in self.information:
            flds = dataclasses.fields(inf)
            infdict = dataclasses.asdict(inf)
            infoline = [f"{f.name}={infdict[f.name]}" for f in flds]
            stream.write(f"{type(inf).__name__}: {', '.join(infoline)}\n")


class JsonOutputter(ABCOutput):
    def write(self, stream: IO[str]):
        classifications: set = set()
        for inf in self.information:
            classifications = classifications.union([type(inf).__name__])
        d = {}
        for c in classifications:
            infdictarray = [dataclasses.asdict(inf) for inf in self.information if c == type(inf).__name__]
            d[c] = infdictarray
        stream.write(json.dumps(d, indent=2))


class CsvOutputter(ABCOutput):
    def write(self, stream: IO[str]):
        col: set = set()
        for inf in self.information:
            col = col.union([type(inf).__name__])
        csv_writer = csv.writer(stream, dialect="excel")
        csv_writer.writerow(col)
        csv_writer.writerows(self.information)
