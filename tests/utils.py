import pathlib
import random
from typing import List, Optional

from steamingpile import interfaces
from steamingpile import types


alpha = "abcdefghijklmnopqrstuvwxyz"
numeric = "1234567890"
punctuation = "_- "


def get_random_name(
    include_punctuation: bool = True, length_min: int = 4, length_max: int = 12, selection_set: Optional[str] = None
) -> str:
    """Return a random name of length between min and max made up of [a-zA-Z0-9 _-]."""

    if selection_set is None:
        selection_set = alpha + alpha.upper() + numeric + punctuation

    name_len = length_min
    if length_min < length_max:
        name_len = random.choice(range(length_min, length_max))
    return "".join(random.sample(selection_set, name_len))


def get_random_id():
    return get_random_name(include_punctuation=False, length_min=10, length_max=10, selection_set=numeric + "ABCDEF")


def get_random_friends(count: int = 1) -> List[types.FriendInformation]:
    return [types.FriendInformation(name=get_random_name(), user_id=get_random_id()) for i in range(count)]


def get_random_games(count: int = 1) -> List[types.GameInformation]:
    return [types.GameInformation(name=get_random_name(), appid=get_random_id()) for i in range(count)]


def get_friends(count: int = 1, name_prefix: str = "Friend ") -> List[types.FriendInformation]:
    return [types.FriendInformation(name=f"{name_prefix}{i + 1}", user_id=f"{i:10X}") for i in range(count)]


def get_games(count: int = 1, game_name_prefix: str = "Game ") -> List[types.GameInformation]:
    return [types.GameInformation(name=f"{game_name_prefix}{i + 1:03d}", appid=f"{i + 1:010X}") for i in range(count)]


class Config(interfaces.IConfiguration):
    """Mocked out configuration implementation for testing purposes."""

    api_key_val = ""
    command_val = ""
    output_file_val = pathlib.Path().home()
    output_format_val = "text"
    passwd_val = "passwd"
    user_val = "user"
    cache_path_val = pathlib.Path().cwd()
    stdout_enabled = True

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

    @property
    def enable_stdout(self) -> bool:
        return self.stdout_enabled

    @enable_stdout.setter
    def enable_stdout(self, value: bool):
        self.stdout_enabled = value

    def print(self):
        return "Testing config object only"


class NoneClientProvider(interfaces.IClientProvider):
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
    get_friends_forced = False
    get_games_forced = False
    get_user_id_forced = False
    get_user_id_friend_name = ""

    def get_cached_friends(self) -> Optional[List[types.FriendInformation]]:
        return self.set_friends

    def get_friends(self, force: bool = False) -> List[types.FriendInformation]:
        self.get_friends_forced = force
        return self.set_friends

    def get_cached_games(self, user_id: str) -> Optional[List[types.GameInformation]]:
        return self.set_games

    def get_games(self, user_id: str, force: bool = False) -> List[types.GameInformation]:
        self.get_games_forced = force
        return self.set_games

    def get_user_id(self, friend_name: str = "", force: bool = False) -> str:
        self.get_user_id_forced = force
        self.get_user_id_friend_name = friend_name
        return self.set_user_id
