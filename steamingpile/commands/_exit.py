from typing import List

from . import _abc
from steamingpile import interfaces
from steamingpile import types


class Exit(_abc.Command):
    """Log out from Steam and exit the steamingpile application."""

    def __init__(self, cfg: interfaces.IConfiguration):
        super().__init__(cfg)

    def run(self, arguments: str, client_provider: interfaces.IClientProvider) -> List[str]:
        """Exit the app by raising the SteamingExit exception."""
        raise types.SteamingExit
