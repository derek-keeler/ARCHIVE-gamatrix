"""Ensure each command is present in the main app."""
import pytest  # type: ignore

from steamingpile import commands
from steamingpile import types

from . import utils


def test_get_command_with_args():
    """Get a legit command back, along with the arguments sent in."""
    cmd, args = commands.get_command("exit --blah --de-blah", utils.Config())
    assert cmd
    assert isinstance(cmd, commands.Exit)
    assert args == "--blah --de-blah"


def test_get_command_with_quoted_arg():
    """Get a legit command back, along with the arguments sent in."""
    cmd, args = commands.get_command("exit --foo='bar'", utils.Config())
    assert cmd
    assert isinstance(cmd, commands.Exit)
    assert args == "--foo='bar'"


def test_get_fully_quoted_command_with_arg():
    """Get a legit command back, along with the arguments sent in."""
    cmd, args = commands.get_command("\"exit --foo='bar'\"", utils.Config())
    assert cmd
    assert isinstance(cmd, commands.Exit)
    assert args == "--foo='bar'"


def test_command_exit_exception():
    """Exit command raises the SteamingExit exception."""
    exit_command = commands.Exit(utils.Config())
    with pytest.raises(types.SteamingExit):
        exit_command.run("", utils.NoneClientProvider())


def test_command_unknown():
    """Ensure the unknown command takes the incorrect command and returns it in the output explanaition."""
    unkown_command = commands.Unknown(utils.Config())
    non_cmd_name = "beets, bears, battlestar galactica"
    result = unkown_command.run(non_cmd_name, utils.NoneClientProvider())
    assert result[0].find(non_cmd_name) != -1
