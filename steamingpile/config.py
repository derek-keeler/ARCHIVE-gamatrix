"""Configuration values used during the runtime of Steamingpile."""

import os
import pathlib
from typing import List, Optional

from . import interfaces

SupportedOutputTypes = ("csv", "json", "text")

API_KEY_ENV_VAR_NAME = "USER_STEAM_API_DEV_KEY"
API_KEY_DOTFILE_NAME = ".user_steam_api_dev_key"


class SteamingPileConfig(interfaces.IConfiguration):
    def __init__(self, args: dict):
        self.args = args
        self._api_key: Optional[str] = None

    def user(self) -> str:
        return self.args["--user"]

    def passwd(self) -> str:
        return self.args["--passwd"]

    def command(self) -> str:
        return self.args["--command"]

    @property
    def output_format(self) -> str:
        for ot in SupportedOutputTypes:
            if ot.value == self.args["--output-format"]:
                return ot.value
        return SupportedOutputTypes.TEXT.value

    @output_format.setter
    def output_format(self, value: str):
        if value in SupportedOutputTypes:
            self.args["--output-format"] = value
        else:
            print(f"Given format type '{value}' not a valid type. See help for valid formats.")

    @property
    def output_file(self) -> Optional[pathlib.Path]:
        file_path: Optional[pathlib.Path] = None
        if "--output-file" in self.args and self.args["--output-file"]:
            try:
                file_path = pathlib.Path(self.args["--output-file"])
            except Exception as e:
                print(e)
                self.output_file = None
        return file_path

    @output_file.setter
    def output_file(self, value: pathlib.Path):
        if value is not None:
            self.args["--output-file"] = value.as_uri()
        else:
            self.args["--output-file"] = None

    def api_key(self) -> str:
        """Get the API key from the command line, environment variable, or dotfile."""
        if self._api_key is None:
            self._api_key = self._get_api_key(self.args["--user-steam-api-dev-key"])
        return self._api_key

    def cache_path(self) -> pathlib.Path:
        """Return the directory where we should store this user's cached data."""
        return pathlib.Path.home().joinpath(".steamingpile/")

    @property
    def enable_stdout(self) -> bool:
        return not self.args["--quiet"]

    @enable_stdout.setter
    def enable_stdout(self, value: bool):
        self.args["--quiet"] = not value

    def print(self) -> List[str]:
        """Return a list of printable strings representing the current config."""
        return [
            f"{key.strip('-')}{'.' * (80 - len(key.strip('-')) - len(str(self.args[key])))}{str(self.args[key])}"
            for key in self.args.keys()
        ]

    def _get_api_key(self, cmdline_key: str = None) -> str:
        """Return the API Dev key supplied by Steam to this user, or None."""

        if cmdline_key is None or cmdline_key == "":
            # read the environment variable USER_STEAM_API_DEV_KEY
            cmdline_key = os.getenv(API_KEY_ENV_VAR_NAME)

        if cmdline_key is None or cmdline_key == "":
            chk_file = pathlib.Path(API_KEY_DOTFILE_NAME)
            if chk_file.is_file():
                with open(API_KEY_DOTFILE_NAME, "r") as f:
                    cmdline_key = f.readline().strip()

        return cmdline_key or ""
