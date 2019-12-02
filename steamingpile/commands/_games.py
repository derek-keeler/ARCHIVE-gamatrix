from typing import List

from . import _abc

from steamingpile import interfaces

GAMES_CMD_VERSION = "0.1"


class Games(_abc.Command):
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

    def __init__(self):
        super().__init__()

    def version(self) -> str:
        return GAMES_CMD_VERSION

    def run_impl(
        self, options: dict, config: interfaces.IConfiguration, client: interfaces.IClientProvider
    ) -> List[str]:
        """Return the list of stored friend information."""

        user_id_to_get_games_for = client.get_user_id(friend_name=options["--friend"], force=options["--force"])

        game_info = client.get_games(user_id=user_id_to_get_games_for, force=options["--force"])

        return sorted([f"{g.name} [appid:{g.appid}]" for g in game_info], key=str.lower)
