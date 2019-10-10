from steamingpile.commands.steaming_pile_command import SteamingPileCommand


class SPUnknownCommand(SteamingPileCommand):
    def __init__(self, cfg):
        super().__init__(cfg)

    @property
    def command_id(self) -> str:
        return "unknown"

    @property
    def requires_client(self) -> bool:
        return False

    def run(self, arguments: str) -> [str]:
        """Tell the user the command they issued is unknown and tell them about help."""

        command = ""
        if arguments:
            command = f"'{arguments}'"

        return [f"Unkown argument {command}.", "Please use the 'help' command to see available commands"]

    def help_brief(self):
        return ""
