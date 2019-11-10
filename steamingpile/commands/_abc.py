import abc

from typing import List

from steamingpile import interfaces


class Command(abc.ABC):
    """Base class for all Steaming Pile commands."""

    def __init__(self, cfg: interfaces.IConfiguration):
        self._config = cfg

    def run(self, arguments: str, client_provider: interfaces.IClientProvider) -> List[str]:
        raise NotImplementedError

    def help_brief(self) -> str:
        return self.__doc__ or ""

    def help_detailed(self) -> List[str]:
        return [self.help_brief()]
