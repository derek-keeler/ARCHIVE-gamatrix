from steamingpile.commands.steaming_pile_command import SteamingPileCommand
from steamingpile.steaming_types import SteamingExit


class SPExitCommand(SteamingPileCommand):
    def __init__(self, cfg):
        super().__init__(cfg)

    @property
    def command_id(self) -> str:
        return "exit"

    @property
    def requires_client(self) -> bool:
        return False

    def run(self, arguments: str) -> [str]:
        """Exit the app by raising the SteamingExit exception."""
        raise SteamingExit

    def help_brief(self):
        return "Log out from Steam and exit the steamingpile application."

    def help_detailed(self):
        return self.help_brief()
