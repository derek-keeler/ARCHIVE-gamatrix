from typing import List

from . import _abc
from steamingpile import interfaces


class Unknown(_abc.Command):
    def __init__(self, cfg: interfaces.IConfiguration):
        super().__init__(cfg)

    @property
    def requires_client(self) -> bool:
        return False

    def run(self, arguments: str, client_provider: interfaces.IClientProvider) -> List[str]:
        """Tell the user the command they issued is unknown and tell them about help."""

        command = ""
        if arguments:
            command = f"'{arguments}'"

        return [f"Unkown argument {command}.", "Please use the 'help' command to see available commands"]

    def help_brief(self):
        return ""
