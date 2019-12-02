from typing import List

from . import _abc
from steamingpile import interfaces
from steamingpile import types


class Exit(_abc.Command):
    """ exit
    Log out from Steam and exit the steamingpile application.

    Usage: exit
    """

    def __init__(self):
        super().__init__()

    def run_impl(
        self, options: dict, config: interfaces.IConfiguration, client: interfaces.IClientProvider
    ) -> List[str]:
        """Exit the app by raising the SteamingExit exception."""
        raise types.SteamingExit
