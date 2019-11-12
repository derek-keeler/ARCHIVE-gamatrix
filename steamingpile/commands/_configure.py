"""Command: configure
Change the configuration of the application during runtime.

Usage:
  configure --output-file=FILE
  configure --output-format=FRMT
  configure < --stdout | --no-stdout >
  configure --print

Details:
  -o --output-file=FILE     Send all output to a specified file.
  -f --output-format=FRMT   Set output format to one of JSON, TEXT, or CSV.
  --stdout                  Send all output to stdout and a file specified, if a file has been specified.
  --no-stdout               Stop sending any output to stdout.
  -p --print                Print out the current configuration.

"""  # noqa

import pathlib
from typing import Any, Dict, List, Optional

import docopt

from steamingpile import interfaces

from . import _abc


class Configure(_abc.Command):
    """Change configuration of the application during runtime."""

    def __init__(self, cfg: interfaces.IConfiguration):
        super().__init__(cfg)

    def run(self, arguments: str, client_provider: interfaces.IClientProvider) -> List[str]:
        opt: Dict[str, Any] = {}
        cmd_output = ["Config command result:"]

        try:
            opt = docopt.docopt(__doc__, argv=self.split_arguments(arguments))
        except docopt.DocoptExit:
            cmd_output = [f"ERROR: Unknown options given in command: '{arguments}'."]
            cmd_output.extend(__doc__.splitlines())

        if "--output-file" in opt and opt["--output-file"]:
            self._config.output_file = pathlib.Path(opt["--output-file"])
            cmd_output.append(f"Set output file to '{self._config.output_file.name}'")

        elif "--output-format" in opt and opt["--output-format"]:
            self._config.output_format = opt["--output-format"]
            cmd_output.append(f"Setting output format to {self._config.output_format}")

        elif "--stdout" in opt and opt["--stdout"]:
            self._config.disable_stdout = False
            cmd_output.append("Enabled stdout output during command execution.")

        elif "--no-stdout" in opt and opt["--stdout"]:
            self._config.disable_stdout = True
            cmd_output.append("Disabled stdout output during command execution.")

        elif "--print" in opt and opt["--print"]:
            cmd_output.append(self._config.args)

        return cmd_output
