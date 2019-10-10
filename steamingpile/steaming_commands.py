import enum

from .commands.steaming_pile_command import SteamingPileCommand
from .commands.friends import SPFriendsCommand
from .commands.unknown import SPUnknownCommand
from .commands.exit import SPExitCommand
from .steaming_pile_config import SteamingPileConfig


class SPCommandName(enum.Enum):
    COMPARE = "compare"
    EXIT = "exit"
    FRIEND = "friend"
    FRIENDS = "friends"
    GAMES = "games"
    HELP = "help"
    UNKNOWN = "unknown"


class SteamingCommand:
    """Contains commands that can be run in the SteamingPile app."""

    def __init__(self, config: SteamingPileConfig):
        self._commands = {
            SPCommandName.COMPARE: None,
            SPCommandName.EXIT: SPExitCommand(cfg=config),
            SPCommandName.FRIENDS: SPFriendsCommand(cfg=config),
            SPCommandName.FRIEND: None,
            SPCommandName.HELP: None,
            SPCommandName.GAMES: None,
            SPCommandName.UNKNOWN: SPUnknownCommand(cfg=config),
        }

    def get_command(self, command: str) -> [SteamingPileCommand, str]:
        command_line = command.split(" ", 1)
        command_name = command_line[0]
        arguments = command_line[1:]

        try:
            sp_cmd = SPCommandName(command_name)
        except ValueError:
            sp_cmd = SPCommandName.UNKNOWN
            arguments = command_name

        return self._commands[sp_cmd], arguments
