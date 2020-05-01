from typing import List

import gamatrix.doc as appdoc
from gamatrix import interfaces

from . import _abc


class Help(_abc.Command):
    """ Show help for all commands.
        Usage: help
    """

    def __init__(self):
        super().__init__()

    def run_impl(
        self,
        options: dict,
        config: interfaces.IConfiguration,
        client: interfaces.IClientProvider,
    ) -> List[str]:
        return appdoc.__doc__.split("\n")
