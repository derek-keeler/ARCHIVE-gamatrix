import abc
import json
import csv
import dataclasses
import secrets
import io
from typing import Any, Dict, IO, List, Set


@dataclasses.dataclass
class DataPlayBase:
    pass


@dataclasses.dataclass
class Derek(DataPlayBase):
    age: int
    surname: str


@dataclasses.dataclass
class Rita(DataPlayBase):
    surname: str
    middlename: str


@dataclasses.dataclass
class Brando(DataPlayBase):
    nickname: str
    age: int
    location: str


def play(o: object):
    if not dataclasses.is_dataclass(o):
        print("No, o is not a dataclass. Terminating.")
        return

    print("Yes, o is a dataclass")
    print("Fields:")
    for f in dataclasses.fields(d):
        print(f"Name: {f.name}")


def playlists(all: List[object]):
    fieldlist: Set[str] = set([])
    rows: List[Dict[str, Any]] = []

    for o in all:
        if not dataclasses.is_dataclass(o):
            print("Skipping non-dataclass member of list:")
            print(o)
            continue
        fieldlist = fieldlist.union([fld.name for fld in dataclasses.fields(o)])
        rows.append(dataclasses.asdict(o))
    print("Fields found for all dataclasses given:")
    print(fieldlist)


class IOutputter:
    @property
    def information(self) -> List[DataPlayBase]:
        raise NotImplementedError

    @information.setter
    def information(self, value: List[DataPlayBase]):
        raise NotImplementedError

    def write(self, stream: IO[str]):
        raise NotImplementedError


class ABCOutputter(abc.ABC, IOutputter):
    _info: List[DataPlayBase] = []

    def __init__(self, initial_data: List[DataPlayBase] = []):
        d = []
        if initial_data:
            d = initial_data
        self.information = d

    @property
    def information(self) -> List[DataPlayBase]:
        return self._info

    @information.setter
    def information(self, value: List[DataPlayBase]):
        self._info = value

    @abc.abstractmethod
    def write(to_stream: IO[str]):
        raise NotImplementedError("All subclasses must implement the write method.")


class BasicOutputter(ABCOutputter):
    _info: List[object]

    def __init__(self, initial_data: List[DataPlayBase] = []):
        super().__init__(initial_data)

    def write(self, stream: IO[str]):
        lines = [f"{inf.__str__()}\n" for inf in self.information]
        stream.writelines(lines)


class TextOutputter(ABCOutputter):
    def write(self, stream: IO[str]):
        for inf in self.information:
            flds = dataclasses.fields(inf)
            infdict = dataclasses.asdict(inf)
            infoline = [f"{f.name}={infdict[f.name]}" for f in flds]
            stream.write(f"{type(inf).__name__}: {', '.join(infoline)}\n")


class JsonOutputter(ABCOutputter):
    def write(self, stream: IO[str]):
        classifications: set = set()
        for inf in self.information:
            classifications = classifications.union([type(inf).__name__])
        d = {}
        for c in classifications:
            infdictarray = [dataclasses.asdict(inf) for inf in self.information if c == type(inf).__name__]
            d[c] = infdictarray
        stream.write(json.dumps(d, indent=2))


class CsvOutputter(ABCOutputter):
    def write(self, stream: IO[str]):
        col: set = set()
        for inf in self.information:
            col = col.union([type(inf).__name__])
        csv_writer = csv.writer(stream, dialect="excel")


def do_something(title: str, data: List[DataPlayBase], output: IOutputter):
    output.information = data
    string_stream = io.StringIO(newline="\n")

    output.write(stream=string_stream)

    string_stream.seek(0)
    print("")
    print("-" * len(title))
    print(title)
    print("-" * len(title))
    print("")
    print("".join(string_stream.readlines()))


if __name__ == "__main__":
    d = Derek(age=22, surname="Keeler")
    play(d)

    dereks = [Derek(age=30 + i, surname=f"Keeler_{i}") for i in range(10)]
    ritas = [Rita(surname=f"Tsu_{i}", middlename=f"Middle_{i}") for i in range(3)]
    brandos = [
        Brando(
            nickname=f"Bran{a}",
            age=secrets.choice(range(15, 25)),
            location=secrets.choice(["Japan", "Canada", "China", "America"]),
        )
        for a in ["do", "den", "", "dobean"]
    ]
    ls = dereks + ritas + brandos
    playlists(ls)
    do_something("Show basic output", ls, BasicOutputter())
    do_something("Show text output", ls, TextOutputter())
    do_something("Show JSON output", ls, JsonOutputter())
    do_something("Show CSV output", ls, CsvOutputter())
