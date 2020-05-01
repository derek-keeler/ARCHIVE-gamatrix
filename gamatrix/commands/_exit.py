from typing import List

from gamatrix import interfaces, types

from . import _abc


class Exit(_abc.Command):
    """ exit
    Log out from Steam and exit the gamatrix application.

    Usage: exit
    """

    def __init__(self):
        super().__init__()

    def run_impl(
        self,
        options: dict,
        config: interfaces.IConfiguration,
        client: interfaces.IClientProvider,
    ) -> List[str]:
        """Exit the app by raising the GamatrixExit exception."""
        raise types.GamatrixExit
