"""games

Print out a list of all the games owned by the specified user, or of all
the games owned by the currently logged in user. The user can be specified
by their steam ID or by their steam user name.

Usage:
    games [--force] [--friend=USR]

Options:
    --friend=USR        Specify the user name of the Steam friend to return the games for.
    --force             Get game information for friend and refresh saved game info for that friend.
"""  # noqa501

import docopt  # type: ignore
from typing import List

from . import _abc

from steamingpile import interfaces

GAMES_CMD_VERSION = 0.1


class Games(_abc.Command):
    """Obtain a list of games that a steam friend owns."""

    def __init__(self, cfg: interfaces.IConfiguration):
        super().__init__(cfg)

    def run(self, arguments: str, client_provider: interfaces.IClientProvider) -> List[str]:
        """Return the list of stored friend information."""

        games_opts = docopt.docopt(__doc__, argv=arguments.split(), version=GAMES_CMD_VERSION)

        user_id_to_get_games_for = client_provider.get_user_id(
            friend_name=games_opts["--friend"], force=games_opts["--force"]
        )

        game_info = client_provider.get_games(user_id=user_id_to_get_games_for, force=games_opts["--force"])

        return [f"{g.name} [appid:{g.appid}]" for g in game_info]

    def help_brief(self):
        return "Return a list of all steam games owned"

    def help_detailed(self):
        return self.__doc__
