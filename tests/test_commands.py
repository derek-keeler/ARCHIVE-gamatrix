"""Ensure each command is present in the main app."""
import pytest  # type: ignore

from steamingpile import commands
from steamingpile import types

from . import stubs


def test_command_exit_exception():
    """Exit command raises the SteamingExit exception."""
    exit_command = commands.Exit(stubs.Config())
    with pytest.raises(types.SteamingExit):
        exit_command.run("", stubs.NoneCientProvider())


def test_command_unknown():
    """Ensure the unknown command takes the incorrect command and returns it in the output explanaition."""
    unkown_command = commands.Unknown(stubs.Config())
    non_cmd_name = "beets, bears, battlestar galactica"
    result = unkown_command.run(non_cmd_name, stubs.NoneCientProvider())
    assert result[0].find(non_cmd_name) != -1
