import functools
from typing import Dict, Optional

from ._abc import Command  # noqa F401
from ._compare import Compare
from ._exit import Exit
from ._friends import Friends
from ._games import Games
from ._help import Help


def get_command(command: str) -> Optional[Command]:
    """Ensure the command issued is one we support else return 'Unknown' command to notify user."""

    cmd_map = _mapping()
    cmd = None
    command_name = command.lower()

    if command_name in cmd_map:
        cmd = cmd_map[command_name]

    return cmd


@functools.lru_cache()
def _mapping() -> Dict:
    """Get a command object based on its name. Cached to not continuously get new objects."""
    _command_mapping: Dict[str, Command] = {
        cls.__name__.lower(): cls() for cls in (Compare, Exit, Friends, Games, Help)
    }
    return _command_mapping
