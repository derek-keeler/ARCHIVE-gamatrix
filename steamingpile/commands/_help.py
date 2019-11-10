from typing import List

from steamingpile import interfaces

from . import _abc


class Help(_abc.Command):
    """Show help for all commands."""

    def __init__(self, cfg: interfaces.IConfiguration):
        super().__init__(cfg)

    def run(self, arguments: str, client_provider: interfaces.IClientProvider) -> List[str]:
        return ["Show help here."]
