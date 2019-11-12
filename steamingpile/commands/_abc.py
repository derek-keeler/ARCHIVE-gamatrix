import abc

from typing import List

from steamingpile import interfaces


class Command(abc.ABC):
    """Base class for all Steaming Pile commands."""

    def __init__(self, cfg: interfaces.IConfiguration):
        self._config = cfg

    def cmdline_parse_args(self, arguments: str) -> List[str]:
        """Parse a commandline similar to how the `main(argc, argv)` would have been parsed."""

        # We need to split this command line in an odd way to handle friends who have spaces in their names
        # split on the argument moniker '--' and try and put it back in front of each occurrance, and then
        # remove any quotes used in individual arguments that we split out.
        args_split = [f"--{a.strip()}" for a in arguments.split("--")]
        args_split = [a.replace('"', "").replace("'", "") for a in args_split]
        # filter out any '--' elements left lying around...
        return list(filter(lambda a: a != "--", args_split))

    def run(self, arguments: str, client_provider: interfaces.IClientProvider) -> List[str]:
        raise NotImplementedError

    def help_brief(self) -> str:
        return self.__doc__ or ""

    def help_detailed(self) -> List[str]:
        return [self.help_brief()]

    def split_arguments(self, arguments: str) -> List[str]:
        """Split a command line to handle arguments that may have spaces in their values."""

        # Split on the argument moniker '--' and try and put it back in front of each occurrance
        args_split = [f"--{a.strip()}" for a in arguments.split("--")]

        # filter out any '--' elements left lying around
        return list(filter(lambda a: a != "--", args_split))
