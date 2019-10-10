"""Ensure each command is present in the main app."""

from steamingpile.steaming_commands import SPCommandName, SteamingCommand


def test_command_help():
    sc = SteamingCommand()
    help_command = sc.get_command(SPCommandName.HELP)
    help_command.initialize(None)
    help_command.run(None)
