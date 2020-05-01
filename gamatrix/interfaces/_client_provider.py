import abc
from typing import List, Optional

from gamatrix import types


class IClientProvider(abc.ABC):
    """Implementation of a class that provides a game client."""

    def get_cached_friends(self) -> Optional[List[types.FriendInformation]]:
        """Return a list of information about gaming friends for the logged-in user."""
        raise NotImplementedError

    def get_friends(self, force: bool = False) -> List[types.FriendInformation]:
        """Return a list of information about gaming friends for the logged-in user."""
        raise NotImplementedError

    def get_cached_games(self, user_id: str) -> Optional[List[types.GameInformation]]:
        """Return a list of game information previously cached for the named user."""
        raise NotImplementedError

    def get_games(
        self, user_id: str, force: bool = False
    ) -> List[types.GameInformation]:
        """Return a list of game information owned by the user specified."""
        raise NotImplementedError

    def get_user_id(self, friend_name: str = "", force: bool = False) -> str:
        """Returns the game-client user id for the friend, or the logged in user."""
        raise NotImplementedError
