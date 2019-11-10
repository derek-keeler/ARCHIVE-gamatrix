import pathlib
from typing import List, Optional

from steamingpile import interfaces
from steamingpile import types


class Config(interfaces.IConfiguration):
    """Mocked out configuration implementation for testing purposes."""

    api_key_val = ""
    command_val = ""
    output_file_val = pathlib.Path().home()
    output_format_val = "text"
    passwd_val = "passwd"
    user_val = "user"
    cache_path_val = pathlib.Path().cwd()

    def api_key(self) -> str:
        return self.api_key_val

    def command(self) -> str:
        return self.command_val

    def output_file(self) -> pathlib.Path:
        return self.output_file_val

    def output_format(self) -> str:
        return self.output_format_val

    def passwd(self) -> str:
        return self.passwd_val

    def user(self) -> str:
        return self.user_val

    def cache_path(self) -> pathlib.Path:
        return self.cache_path_val


class NoneCientProvider(interfaces.IClientProvider):
    """Mock client provider that returns None for each request for a client."""

    def get_cached_friends(self) -> Optional[List[types.FriendInformation]]:
        return None

    def get_friends(self):
        return []

    def get_cached_games(self, user_id: str) -> Optional[List[types.GameInformation]]:
        return []

    def get_games(self, user_id: str, force: bool = False) -> List[types.GameInformation]:
        return []

    def get_user_id(self, friend_name: str = "", force: bool = False) -> str:
        return ""


class SettableClientProvider(interfaces.IClientProvider):
    """Mock client provider that allows tests to set the values to return."""

    set_friends: List[types.FriendInformation] = []
    set_games: List[types.GameInformation] = []
    set_user_id: str = ""

    def get_cached_friends(self) -> Optional[List[types.FriendInformation]]:
        return self.set_friends

    def get_friends(self, force: bool = False) -> List[types.FriendInformation]:
        return self.set_friends

    def get_cached_games(self, user_id: str) -> Optional[List[types.GameInformation]]:
        return self.set_games

    def get_games(self, user_id: str, force: bool = False) -> List[types.GameInformation]:
        return self.set_games

    def get_user_id(self, friend_name: str = "", force: bool = False) -> str:
        return self.set_user_id
