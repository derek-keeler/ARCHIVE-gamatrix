import abc

from typing import List, Optional

from steamingpile import interfaces


class Command(abc.ABC):
    """Base class for all Steaming Pile commands."""

    _output_impl: Optional[interfaces.ICommandOutput] = None

    def __init__(self, cfg: interfaces.IConfiguration):
        self._config = cfg

    def run(self, arguments: str, client_provider: interfaces.IClientProvider) -> List[str]:
        raise NotImplementedError

    def help_brief(self) -> str:
        return self.__doc__ or ""

    def help_detailed(self) -> List[str]:
        return [self.help_brief()]

    @property
    def output(self) -> interfaces.ICommandOutput:
        if not self._output_impl:
            raise TypeError(
                f"Command object {self.__name__}'s output member has not been given a CommandOutput implementation."
            )
        return self._output_impl

    @output.setter
    def output(self, impl: interfaces.ICommandOutput):
        self._output_impl = impl
