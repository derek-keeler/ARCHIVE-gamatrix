"""Configuration values used during the runtime of Steamingpile."""

import enum
import os
import pathlib
from typing import List, Optional

from . import interfaces


class SupportedOutputTypes(enum.Enum):
    JSON = "json"
    TEXT = "txt"
    CSV = "csv"


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

    def command(self) -> Optional[str]:
        return self.args["<cmd>"]

    def command_args(self) -> List[str]:
        return self.args["<args>"] or []

    def output_format(self) -> str:
        for ot in SupportedOutputTypes:
            if ot.value == self.args["--output-format"]:
                return ot.value
        return SupportedOutputTypes.TEXT.value

    def output_file(self) -> pathlib.Path:
        return pathlib.Path(self.args["--output-file"])

    @property
    def force(self) -> bool:
        return self.args["--force"]

    def api_key(self) -> str:
        """Get the API key from the command line, environment variable, or dotfile."""
        if self._api_key is None:
            self._api_key = self._get_api_key(self.args["--user-steam-api-dev-key"])
        return self._api_key

    def config_path(self) -> pathlib.Path:
        """Return the directory where we should store this user's configuration data."""
        return pathlib.Path.home().joinpath(".steamingpile/")

    def cache_path(self) -> pathlib.Path:
        """Return the directory where we should store this user's cached data."""
        return self.config_path().joinpath(".steamingpile/cache")

    def _get_api_key(self, cmdline_key: str = None) -> str:
        """Return the API Dev key supplied by Steam to this user, or None."""

        if cmdline_key is None or cmdline_key == "":
            # read the environment variable USER_STEAM_API_DEV_KEY
            cmdline_key = os.getenv(API_KEY_ENV_VAR_NAME)

        if cmdline_key is None or cmdline_key == "":
            chk_file = self.config_path().joinpath(API_KEY_DOTFILE_NAME)
            if chk_file.is_file():
                with open(chk_file, "r") as f:
                    cmdline_key = f.readline().strip()

        return cmdline_key or ""
