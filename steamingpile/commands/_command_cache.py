import functools
from typing import Dict, Tuple

from ._abc import Command  # noqa F401
from ._compare import Compare
from ._configure import Configure
from ._exit import Exit
from ._friends import Friends
from ._games import Games
from ._help import Help
from ._unknown import Unknown
from steamingpile import interfaces


def get_command(command: str, config: interfaces.IConfiguration) -> Tuple[Command, str]:
    """Ensure the command issued is one we support else return 'Unknown' command to notify user."""

    while command[0] == command[-1] and command.startswith(('"', "'")):
        command = command[1:-1]

    command_name, _, arguments = command.partition(" ")  # strip("\"' ")
    cmd_map = _mapping(config)
    cmd = None
    if command_name.lower() in cmd_map:
        cmd = cmd_map[command_name.lower()]
    if cmd is None:
        cmd = cmd_map["unknown"]
        arguments = command_name
    return cmd, arguments


@functools.lru_cache()
def _mapping(config: interfaces.IConfiguration) -> Dict:
    """Get a command object based on its name. Cached to not continuously get new objects."""
    _command_mapping: Dict[str, Command] = {
        cls.__name__.lower(): cls(cfg=config) for cls in (Compare, Configure, Exit, Friends, Games, Help, Unknown)
    }
    return _command_mapping
