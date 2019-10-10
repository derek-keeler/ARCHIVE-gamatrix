from steamingpile.commands.steaming_pile_command import SteamingPileCommand


class SPFriendsCommand(SteamingPileCommand):
    def __init__(self, cfg):
        super().__init__(cfg)
        self._friends_list = None

    @property
    def command_id(self) -> str:
        return "friends"

    def run(self, arguments: str) -> [str]:
        """Return the list of stored friend information."""
        if self._steam_client is None:
            raise Exception("Friends command requires Steam login first.")

        self.cache_friends()
        return self._friends_list.values()

    def cache_friends(self):
        """Collect all pertinent friend information and store it in a list, unless we've done it before."""
        if self._friends_list is None:
            self._friends_list = {}
            for friend in self._steam_client.friends:
                self._friends_list[friend.steam_id] = f"{friend.name}: [${friend.steam_id}]"

    def help_brief(self):
        return "Return a list of all steam friends and their steam ids."
