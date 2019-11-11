from typing import List

import steamingpile.doc as appdoc
from steamingpile import interfaces

from . import _abc


class Help(_abc.Command):
    """Show help for all commands."""

    def __init__(self, cfg: interfaces.IConfiguration):
        super().__init__(cfg)

    def run(self, arguments: str, client_provider: interfaces.IClientProvider) -> List[str]:
        return appdoc.__doc__.split("\n")
