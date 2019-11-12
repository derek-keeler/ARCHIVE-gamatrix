"""Interface for configuration values used by the steamingpile program."""

import abc
import pathlib
from typing import List, Optional


class IConfiguration(abc.ABC):
    @abc.abstractmethod
    def user(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def passwd(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def command(self) -> Optional[str]:
        raise NotImplementedError

    @abc.abstractmethod
    def command_args(self) -> List[str]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def output_format(self) -> str:
        raise NotImplementedError

    @output_format.setter
    def output_format(self, value: str):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def output_file(self) -> pathlib.Path:
        raise NotImplementedError

    @output_file.setter
    def output_file(self, value: pathlib.Path):
        raise NotImplementedError

    @abc.abstractmethod
    def api_key(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def config_path(self) -> pathlib.Path:
        """Return the directory where we should store this user's configuration data."""
        raise NotImplementedError

    @abc.abstractmethod
    def cache_path(self) -> pathlib.Path:
        """Return the directory where we should store this user's cached data."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def force(self) -> bool:
        """Did the user set the global option to force retrieval from the game service?"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def disable_stdout(self) -> bool:
        raise NotImplementedError

    @disable_stdout.setter
    def disable_stdout(self, value: bool):
        raise NotImplementedError

    @abc.abstractmethod
    def print(self) -> List[str]:
        raise NotImplementedError
