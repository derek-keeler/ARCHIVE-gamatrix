import abc
from typing import List

import docopt  # type: ignore

from steamingpile import interfaces


COMMAND_MODULE_VERSION = "0.2"


class Command(abc.ABC):
    """Base class for all Steaming Pile commands."""

    def __init__(self):
        pass

    @property
    def version(self) -> str:
        """Return the version of a specific command if this is overridden, otherwise the COMMAND_MODULE_VERSION."""
        return COMMAND_MODULE_VERSION

    def run_impl(
        self, options: dict, config: interfaces.IConfiguration, client: interfaces.IClientProvider
    ) -> List[str]:
        """The actual run implementation for each command."""
        raise NotImplementedError

    def run(self, cfg: interfaces.IConfiguration, client_provider: interfaces.IClientProvider) -> List[str]:
        """Run the command, given the command name issued and using the configuration given."""
        return self.run_impl(
            options=docopt.docopt(self.__doc__, argv=cfg.command_args(), version=self.version),
            config=cfg,
            client=client_provider,
        )
