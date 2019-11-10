"""Interface for configuration values used by the steamingpile program."""

import abc
import pathlib


class IConfiguration(abc.ABC):
    @abc.abstractmethod
    def user(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def passwd(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def command(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def output_format(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def output_file(self) -> pathlib.Path:
        raise NotImplementedError

    @abc.abstractmethod
    def api_key(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def cache_path(self) -> pathlib.Path:
        raise NotImplementedError
