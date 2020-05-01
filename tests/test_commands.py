"""Ensure each command is present in the main app."""
import pytest  # type: ignore

from gamatrix import commands
from gamatrix import types

from . import utils


def test_get_command_with_args():
    """Get a legit command back."""
    cmd = commands.get_command("exit")
    assert cmd
    assert isinstance(cmd, commands.Exit)


def test_command_exit_exception():
    """Exit command raises the GamatrixExit exception."""
    exit_command = commands.get_command("exit")
    cfg = utils.Config()
    cfg.command_args_val = []
    with pytest.raises(types.GamatrixExit):
        exit_command.run(utils.Config(), utils.NoneClientProvider())


def test_command_unknown():
    """Ensure unknown commands are handled without exceptions."""
    unkown_command = commands.get_command("no_command_here")
    assert unkown_command is None
