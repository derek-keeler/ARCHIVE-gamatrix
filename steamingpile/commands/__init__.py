import enum

from ._abc import Command  # noqa F401

from ._exit import Exit  # noqa F401
from ._friends import Friends  # noqa F401
from ._games import Games  # noqa F401
from ._unknown import Unknown  # noqa F401

from ._command_cache import get_command  # noqa F401


class Names(enum.Enum):
    # COMPARE = "compare"
    EXIT = "exit"
    # FRIEND = "friend"
    FRIENDS = "friends"
    GAMES = "games"
    # HELP = "help"
    UNKNOWN = "unknown"
