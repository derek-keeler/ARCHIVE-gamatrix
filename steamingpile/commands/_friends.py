from typing import List

from . import _abc
from steamingpile import interfaces


class Friends(_abc.Command):
    """Return a list of all steam friends and their steam ids."""

    def __init__(self, cfg: interfaces.IConfiguration):
        super().__init__(cfg)

    def run(self, arguments: str, client_provider: interfaces.IClientProvider) -> List[str]:
        """Return the list of stored friend information."""
        force_update_friends = arguments.find("--force") > -1
        friends_list = client_provider.get_friends(force=force_update_friends)

        return [f"{f.name} [{f.user_id}]" for f in friends_list]

    def help_detailed(self) -> List[str]:
        return ["--force", "Re-read the friends list from Steam, resetting the cache."]
