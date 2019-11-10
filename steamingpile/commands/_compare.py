""" Print out a list of all the games owned by the specified user, or of all
the games owned by the currently logged in user. The user can be specified
by their steam ID or by their steam user name.

Usage:
    compare --friend=USER ... [--force]

Options:
    --friend=USER     Specify the user name of the game client friend to compare the games with,
                       multiple separated by commas.
    --force            Force a refresh of information from the game client.
"""

import dataclasses
from typing import Any, Dict, List

import docopt  # type: ignore

from . import _abc

from steamingpile import interfaces
from steamingpile import types

COMPARE_CMD_VERSION = 0.1


@dataclasses.dataclass
class CompareCmdOptions:
    friends: List[str]


@dataclasses.dataclass
class FriendGameComparison:
    game_id: str
    game_name: str
    owned_by: List[types.FriendInformation]


class Compare(_abc.Command):
    def __init__(self, cfg: interfaces.IConfiguration):
        super().__init__(cfg)

    def run(self, arguments: str, client_provider: interfaces.IClientProvider) -> List[str]:
        """Compare the logged-in user's games to the friends specified."""
        # We need to split this command line in an odd way to handle friends who have spaces in their names
        # split on the argument moniker '--' and try and put it back in front of each occurrance
        args_split = [f"--{a.strip()}" for a in arguments.split("--")]
        # filter out any '--' elements left lying around
        args = list(filter(lambda a: a != "--", args_split))

        opt = docopt.docopt(__doc__, argv=args, version=COMPARE_CMD_VERSION)

        # Add myself to the beginning of the list
        friends = client_provider.get_friends(force=opt["--force"])
        comparison_friend_names = [f.strip("'").strip('"') for f in opt["--friend"]]
        compare_friends: List[types.FriendInformation] = []
        for f in friends:
            if f.name in comparison_friend_names and f.name not in compare_friends:
                compare_friends.append(f)

        game_list: Dict[str, FriendGameComparison] = {}

        for friend in compare_friends:

            friend_games = client_provider.get_games(user_id=friend.user_id, force=opt["--force"])

            for game in friend_games:
                if game.appid in game_list:
                    game_list[game.appid].owned_by.append(friend)
                else:
                    game_list[game.appid] = FriendGameComparison(
                        game_id=game.appid, game_name=game.name, owned_by=[friend]
                    )

        # flatten this list

        title_row = ["Game"]
        games_by_num_owners: List[List[Any]] = []
        for i in range(len(compare_friends)):
            games_by_num_owners.append([])

        for key in game_list.keys():
            current_game = game_list[key]
            game_row: List[Any] = [f'"{current_game.game_name}"']  # add quotes to satisfy CSV nonsense
            owned_by_counter = 0
            for friend in compare_friends:
                if len(title_row) < len(compare_friends) + 1:
                    title_row.append(f'"{friend.name}"')  # again, sigh
                game_row.append(friend in current_game.owned_by)
                owned_by_counter = owned_by_counter + int(friend in current_game.owned_by)
            games_by_num_owners[owned_by_counter - 1].append(game_row)

        # start building the output.
        gol = [title_row]
        gol.append([f"OWNED BY ALL FRIENDS (count={len(games_by_num_owners[len(compare_friends) - 1])})"])
        gol.extend(games_by_num_owners[len(compare_friends) - 1])

        index = len(compare_friends) - 2
        while index >= 0:
            gol.append([f"OWNED BY {index+1} FRIENDS (count={len(games_by_num_owners[index])})"])
            gol.extend(games_by_num_owners[index])
            index = index - 1

        return [",".join(str(item) for item in row) for row in gol]
