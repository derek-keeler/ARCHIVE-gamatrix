"""games

Print out a list of all the games owned by the specified user, or of all
the games owned by the currently logged in user. The user can be specified
by their steam ID or by their steam user name.

Usage:
    games                               Show all the games the logged-in user owns.
    games (-u <usr> | --user=<usr>)     Show all the games the specified user owns,
                                        user is specified by their steam user name.
    games (-s <sid> | --steam-id=<sid>) Show all the games owned by the specified user
                                        where the user is specified by their steam id.
    games (-f | --force)                Update the games list regardless of whether or 
                                        not a local cache exists.
"""
import docopt

from steam.client import SteamClient
from steam.client.user import SteamUser
from steam.webapi import WebAPI

from steamingpile.commands.steaming_pile_command import SteamingPileCommand

GAMES_CMD_VERSION = 0.1


class SPFriendsCommand(SteamingPileCommand):
    def __init__(self, cfg):
        super().__init__(cfg)
        self._games_list = None

    @property
    def command_id(self) -> str:
        return "games"

    def run(self, arguments: str) -> [str]:
        """Return the list of stored friend information."""
        if self._steam_client is None:
            raise Exception("Friends command requires Steam login first.")

        games_opts = docopt.docopt(self.__doc__, argv=arguments.split(), help=False, version=GAMES_CMD_VERSION)

        steam_user = games_opts["--user"]
        steam_id = games_opts["--steam-id"]
        if not steam_user and not steam_id:
            steam_id = self._steam_client.steam_id
        self.cache_games(
            force=games_opts["--force"], steam_user=games_opts["--user"], steam_id=games_opts["--steam-id"]
        )

        return self._games_list.values()

    def cache_games(self, steam_user: str, steam_id: str, force: bool = False):
        """Collect all pertinent friend information and store it in a list, unless we've done it before."""
        if self._games_list is None or force:
            self._games_list = {}
            s_user = self._steam_client.user
            if steam_id:
                s_user = self._steam_client.get_user(steam_id=steam_id, fetch_persona_state=False)
            self.get_games_for_user(client=self._steam_client, user=s_user, api_key=self._config.api_key)

    def help_brief(self):
        return "Return a list of all steam games owned"

    def help_detailed(self):
        return self.__doc__

    def get_games_for_user(self, client: SteamClient, user: SteamUser, api_key: str) -> dict:
        """Use a steam client instance to get a list of owned games for a user."""
        api = WebAPI(key=api_key)
        response = api.call(
            "IPlayerService.GetOwnedGames",
            key=api_key,
            steamid=user.steam_id,
            include_appinfo=True,
            include_played_free_games=False,
            appids_filter=None,
        )
        r = response["response"]
        games = {g["appid"]: {"name": g["name"]} for g in r["games"]}

        return games
