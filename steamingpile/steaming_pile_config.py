"""Configuration values used during the runtime of Steamingpile."""

import abc
import enum
import os
import pathlib


class SPOutputType(enum.Enum):
    JSON = "json"
    TEXT = "txt"
    CSV = "csv"


API_KEY_ENV_VAR_NAME = "USER_STEAM_API_DEV_KEY"
API_KEY_DOTFILE_NAME = ".user_steam_api_dev_key"


class SteamingPileConfig(abc.ABC):
    def __init__(self, args: dict):
        self.args = args

    @property
    def user(self) -> str:
        return self.args["--user"]

    @property
    def passwd(self) -> str:
        return self.args["--passwd"]

    @property
    def command(self) -> str:
        return self.args["--command"]

    @property
    def output_format(self) -> SPOutputType:
        for ot in SPOutputType:
            if ot == self.args["--output-format"]:
                return ot
        return SPOutputType[0]

    @property
    def output_file(self) -> pathlib.Path:
        return pathlib.Path(self.args["--output-file"])

    @property
    def api_key(self) -> str:
        """Get the API key from the command line, environment variable, or dotfile."""
        if self._api_key is None:
            self._api_key = self.get_api_key(self.args["--user-steam-api-dev-key"])
        return self._api_key

    def get_api_key(self, cmdline_key: str = None) -> str:
        """Return the API Dev key supplied by Steam to this user, or None."""

        if cmdline_key is None:
            # read the environment variable USER_STEAM_API_DEV_KEY
            cmdline_key = os.getenv(API_KEY_ENV_VAR_NAME)

        if cmdline_key is None:
            chk_file = pathlib.Path(API_KEY_DOTFILE_NAME)
            if chk_file.is_file():
                with open(API_KEY_DOTFILE_NAME, "r") as f:
                    cmdline_key = f.readline().strip()

        return cmdline_key
