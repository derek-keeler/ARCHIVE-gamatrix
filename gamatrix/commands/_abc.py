import abc
from typing import List

import docopt  # type: ignore

from gamatrix import interfaces


COMMAND_MODULE_VERSION = "0.2"


class Command(abc.ABC):
    """Base class for all Gamatrix Pile commands."""

    def __init__(self):
        pass

    @property
    def version(self) -> str:
        """Return the version of a specific command."""
        return COMMAND_MODULE_VERSION

    def run_impl(
        self,
        options: dict,
        config: interfaces.IConfiguration,
        client: interfaces.IClientProvider,
    ) -> List[str]:
        """The actual run implementation for each command."""
        raise NotImplementedError

    def run(
        self,
        cfg: interfaces.IConfiguration,
        client_provider: interfaces.IClientProvider,
    ) -> List[str]:
        """Run the command, given the command name and configuration."""
        return self.run_impl(
            options=docopt.docopt(
                self.__doc__, argv=cfg.command_args(), version=self.version
            ),
            config=cfg,
            client=client_provider,
        )
