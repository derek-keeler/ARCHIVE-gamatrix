"""Test the games command."""

import steamingpile.commands as spcmd

from . import stubs


def test_get_help():
    """Probably lame but test that the games command returns 'games' in the help text."""
    games_cmd, _ = spcmd.get_command("games", stubs.Config())
    assert games_cmd
    brief = games_cmd.help_brief()
    ext_help = games_cmd.help_detailed()
    assert brief
    assert ext_help
    assert brief.find("games") != -1
    assert ext_help.find("games") != -1


def test_get_games_for_friend():
    """Ensure we can get a game for a friend using the `--commands=` interface."""
    games_cmd, _ = spcmd.get_command("games", stubs.Config())
    cli_provider = stubs.SettableClientProvider()
    cli_provider.set_friends
