"""friends

Return a list of friends connected to the logged in game client user.

Usage:
    friends [--force | <-f>]

Details:

    --force -f      Disregard any previously cached friend data and re-retrieve it from the game client, overwriting
                    the cache for the next run.
"""  # noqa

from typing import List

import docopt  # type: ignore

from . import _abc
from steamingpile import interfaces

FRIENDS_CMD_VERSION = 1.0


class Friends(_abc.Command):
    """Return a list of all steam friends and their steam ids."""

    def __init__(self, cfg: interfaces.IConfiguration):
        super().__init__(cfg)

    def run(self, arguments: str, client_provider: interfaces.IClientProvider) -> List[str]:
        """Return the list of stored friend information."""
        opts = docopt.docopt(__doc__, argv=arguments.split(), version=FRIENDS_CMD_VERSION)
        friends_list = client_provider.get_friends(force=opts["--force"])

        return [f"{f.name} [{f.user_id}]" for f in friends_list]
