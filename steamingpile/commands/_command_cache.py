import functools
from typing import Dict, Tuple

from ._abc import Command  # noqa F401
from ._compare import Compare
from ._exit import Exit
from ._friends import Friends
from ._games import Games
from ._help import Help
from ._unknown import Unknown
from steamingpile import interfaces


def get_command(command: str, config: interfaces.IConfiguration) -> Tuple[Command, str]:
    """Ensure the command issued is one we support else return 'Unknown' command to notify user."""
    command_name, _, arguments = command.strip("\"' ").partition(" ")
    cmd_map = _mapping(config)
    cmd = cmd_map[command_name.lower()]
    if cmd is None:
        cmd = cmd_map["unknown"]
        arguments = command_name
    return cmd, arguments


@functools.lru_cache()
def _mapping(config: interfaces.IConfiguration) -> Dict:
    _command_mapping: Dict[str, Command] = {
        cls.__name__.lower(): cls(cfg=config) for cls in (Compare, Exit, Friends, Games, Help, Unknown)
    }
    return _command_mapping
