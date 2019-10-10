"""Main driver for the SteamingPile program."""

from abc import ABC

from steam.client import SteamClient
from steam.enums import EResult

from .steaming_pile_config import SteamingPileConfig
from .steaming_commands import SteamingCommand, SPCommandName
from .steaming_types import SteamingExit


class SteamingPile(ABC):
    def __init__(self, conf: SteamingPileConfig):
        self.config = conf
        self._steam_client = None
        self.commands = SteamingCommand()

    @property
    def client(self) -> SteamClient:
        """The logged in Steam client to use in querying for information."""
        if self._steam_client is None:
            self._steam_client = self.login_with_2fa(user=self.config.user, passwd=self.config.passwd)

        return self._steam_client

    def login_with_2fa(self, user: str = None, passwd: str = None) -> SteamClient:
        """Login to steam with user and password. API will request 2FA if client has it enabled."""
        client = SteamClient()

        print("One-off login recipe")
        print("-" * 20)

        result = client.cli_login(username=user, password=passwd)

        if result != EResult.OK:
            print("Failed to login: %s" % repr(result))
            raise SystemExit

        print("-" * 20)
        print("Logged on as:", client.user.name)
        print("Community profile:", client.steam_id.community_url)
        print("Last logon:", client.user.last_logon)
        print("Last logoff:", client.user.last_logoff)

        return client

    def run(self):
        if self.config.command != SPCommandName.UNKNOWN:
            cmd, args = self.commands.get_command(self.config.command)
            if cmd.requires_client:
                cmd.set_client(self.client)
            try:
                results = cmd.run(args)
                print(*results, sep="\n")

            except SteamingExit:
                pass

        else:
            self.run_interactive()

    def run_interactive(self):
        """Wait for textual commands to respond to."""

        cmd = input("steamingpile cmd: ")
        keep_accepting_commands = True

        while keep_accepting_commands:
            exec_cmd, arguments = self.commands.get_command(cmd)

            if exec_cmd is not None:
                try:
                    if exec_cmd.requires_client:
                        exec_cmd.set_client(self.client)

                    results = exec_cmd.run(arguments)
                    print(*results, sep="\n")
                    cmd = input("steamingpile cmd: ")

                except SteamingExit:
                    keep_accepting_commands = False
