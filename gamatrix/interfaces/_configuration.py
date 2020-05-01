"""Interface for configuration values used by the gamatrix program."""

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
        """Did the user set the global force option?"""
        raise NotImplementedError
