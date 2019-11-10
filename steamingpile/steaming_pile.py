"""Main driver for the SteamingPile program."""

import pickle
from typing import Dict, List, Optional

import steam.client                 # type: ignore
import steam.enums                  # type: ignore
import steam.webapi                 # type: ignore

from . import interfaces
from . import commands
from . import types


class SteamingPile(interfaces.IClientProvider):

    FriendsCacheFileName = "friends.cache"
    GamesCacheFileName = "games.cache"

    def __init__(self, conf: interfaces.IConfiguration):
        self.config = conf
        self._steam_client = None
        self._friends_list: Optional[List[types.FriendInformation]] = None
        self._games_list: Dict[str, List[types.GameInformation]] = {}

        self.friend_cache_file = conf.cache_path().joinpath(self.FriendsCacheFileName)
        try:
            with open(self.friend_cache_file, "rb") as cached_friends:
                cf = cached_friends.read()
                self._friends_list = self._load_friends_cache(cf)
        except FileNotFoundError:
            print("No cache file found for friends, will retrieve from game client.")

        self.games_cache_file = conf.cache_path().joinpath(self.GamesCacheFileName)
        try:
            with open(self.games_cache_file, "rb") as cached_games:
                cg = cached_games.read()
                self._games_list = self._load_games_cache(cg) or {}
        except FileNotFoundError:
            print("No cache file found for game data, will retrieve from game client.")

    def _load_friends_cache(self, friends_data: bytes) -> Optional[List[types.FriendInformation]]:
        return pickle.loads(friends_data)

    def _load_games_cache(self, games_data: bytes) -> Optional[Dict[str, List[types.GameInformation]]]:
        return pickle.loads(games_data)

    def _store_friends_cache(self) -> Optional[bytes]:
        return pickle.dumps(self._friends_list)

    def _store_games_cache(self) -> Optional[bytes]:
        return pickle.dumps(self._games_list)

    def client(self) -> steam.client.SteamClient:
        """The logged in Steam client to use in querying for information."""
        if self._steam_client is None:
            self._steam_client = self.login_with_2fa(user=self.config.user(), passwd=self.config.passwd())

        return self._steam_client

    def get_cached_friends(self) -> Optional[List[types.FriendInformation]]:
        """Return a list of all known friends from prior calls to the client API."""
        return self._friends_list

    def get_friends(self, force: bool = False) -> List[types.FriendInformation]:
        """Collect all pertinent friend information and store it in a list, unless we've done it before."""
        friends_list = None
        if force is False:
            friends_list = self.get_cached_friends()

        if friends_list is None:
            all_friends = self.client().friends

            # Add all my friends
            friends_list = [
                types.FriendInformation(name=friend.name, user_id=f"{friend.steam_id.as_64}") for friend in all_friends
            ]

            # Inject myself at the top of the list... (I am queried for info too!)
            friends_list.insert(
                0, types.FriendInformation(name=self.client().username, user_id=f"{self.client().steam_id.as_64}")
            )
            self._friends_list = friends_list

        return friends_list

    def get_friend_by_name(self, name: str, force: bool = False) -> Optional[types.FriendInformation]:
        friends = self.get_friends(force=force)
        for friend in friends:
            if friend.name == name:
                return friend
        return None

    def get_user_id(self, friend_name: str = "", force: bool = False) -> str:
        """Return the user id for the friend-name given, or the user id of the logged-in user."""
        if friend_name is None or len(friend_name) <= 0:
            friend_name = self.config.user()
            if friend_name is None or len(friend_name) <= 0:
                friend_name = self.client().username

        users_friend_info = self.get_friend_by_name(name=friend_name, force=force)
        if users_friend_info is not None:
            return users_friend_info.user_id

        return ""

    def get_cached_games(self, user_id: str) -> Optional[List[types.GameInformation]]:
        """Return the list of game information already stored for this user."""
        if user_id in self._games_list:
            return self._games_list[user_id]
        return None

    def get_games(self, user_id: str, force: bool = False) -> List[types.GameInformation]:
        """Use a steam client instance to get a list of owned games for a user."""

        games_list = None

        if not force:
            games_list = self.get_cached_games(user_id=user_id)

        if games_list is None:

            api_key = self.config.api_key()
            api = steam.webapi.WebAPI(key=api_key)
            response = api.call(
                "IPlayerService.GetOwnedGames",
                key=api_key,
                steamid=user_id,
                include_appinfo=True,
                include_played_free_games=True,
                appids_filter=None,
            )
            r = response["response"]

            self._games_list[user_id] = [types.GameInformation(name=g["name"], appid=g["appid"]) for g in r["games"]]
            games_list = self._games_list[user_id]

        return games_list

    def login_with_2fa(self, user: str = None, passwd: str = None) -> steam.client.SteamClient:
        """Login to steam with user and password. API will request 2FA if client has it enabled."""
        client = steam.client.SteamClient()

        print("One-off login recipe")
        print("-" * 20)

        result = client.cli_login(username=user, password=passwd)

        if result != steam.enums.EResult.OK:
            print("Failed to login: %s" % repr(result))
            raise SystemExit

        print("-" * 20)
        print("Logged on as:", client.user.name)
        print("Community profile:", client.steam_id.community_url)
        print("Last logon:", client.user.last_logon)
        print("Last logoff:", client.user.last_logoff)

        return client

    def _do_exit(self):
        """Clean up any running state/close any open resources/store any cached information."""
        friends_data = self._store_friends_cache()
        games_data = self._store_games_cache()

        self.config.cache_path().mkdir(parents=True, exist_ok=True)  # TODO: permissions limit to user

        if friends_data is not None:
            with open(self.config.cache_path().joinpath(self.FriendsCacheFileName), "wb") as out_friends_file:
                out_friends_file.write(friends_data)

        if games_data is not None:
            with open(self.config.cache_path().joinpath(self.GamesCacheFileName), "wb") as out_games_file:
                out_games_file.write(games_data)

    def run(self):
        if self.config.command() and self.config.command() != "":
            cmd, args = commands.get_command(self.config.command(), self.config)
            try:
                results = cmd.run(args, self)
                print(*results, sep="\n")
            except types.SteamingExit:
                pass
        else:
            self.run_interactive()
        self._do_exit()

    def run_interactive(self):
        """Wait for textual commands to respond to."""

        cmd = input("steamingpile cmd: ")
        keep_accepting_commands = True

        while keep_accepting_commands:
            exec_cmd, arguments = commands.get_command(cmd, self.config)

            if exec_cmd is not None:
                try:
                    # if exec_cmd.requires_client:
                    #     exec_cmd.set_client(self.client)

                    # results = exec_cmd.run(arguments)
                    results = exec_cmd.run(arguments, self)

                    print(*results, sep="\n")
                    cmd = input("steamingpile cmd: ")

                except types.SteamingExit:
                    keep_accepting_commands = False
