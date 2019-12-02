"""Friends command module"""

from typing import List

from . import _abc
from steamingpile import interfaces

FRIENDS_CMD_VERSION = "0.3"


class Friends(_abc.Command):
    """friends
    Return a list of friends connected to the logged in game client user.
    Usage:
        friends
    """  # noqa

    def __init__(self):
        super().__init__()

    def version(self) -> str:
        return FRIENDS_CMD_VERSION

    def run_impl(
        self, options: dict, config: interfaces.IConfiguration, client: interfaces.IClientProvider
    ) -> List[str]:
        """Return the list of stored friend information."""
        friends_list = client.get_friends(force=config.force)

        return sorted([f"{f.name} [{f.user_id}]" for f in friends_list], key=str.lower)
