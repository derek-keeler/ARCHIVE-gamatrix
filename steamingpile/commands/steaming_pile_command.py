from abc import ABC, abstractmethod

from steam.client import SteamClient

from steamingpile.steaming_pile_config import SteamingPileConfig


class SteamingPileCommand(ABC):
    """ Base class for all Steaming Pile commands."""

    def __init__(self, cfg: SteamingPileConfig):
        self._steam_client = None
        self._config = cfg

    def set_client(self, steam_client: SteamClient):
        self._steam_client = steam_client

    @property
    def requires_client(self) -> bool:
        return self._steam_client is None

    @abstractmethod
    def run(self, arguments: str) -> [str]:
        pass

    def help_brief(self) -> str:
        return self.__doc__

    def help_detailed(self) -> [str]:
        return [self.help_brief()]
