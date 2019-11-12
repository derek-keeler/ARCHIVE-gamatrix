""" Print out a list of all the games owned by the specified user, or of all
the games owned by the currently logged in user. The user can be specified
by their steam ID or by their steam user name.

Usage:
    compare --friend=USER ... [--force] [--all-owned-games]

Options:
    -f --friend=USER        Specify the user name of the game client friend to compare the games with,
                            multiple separated by commas.
    -F --force              Force a refresh of information from the game client.
    -a --all-owned-games    Only output games that are owned by every friend specified.
"""

import dataclasses
import datetime
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
    owned_by: List[types.FriendInformation]
    game: types.GameInformation


class Compare(_abc.Command):
    def __init__(self, cfg: interfaces.IConfiguration):
        super().__init__(cfg)

    def run(self, arguments: str, client_provider: interfaces.IClientProvider) -> List[str]:
        """Compare the logged-in user's games to the friends specified."""

        args = self.cmdline_parse_args(arguments)

        opt = docopt.docopt(__doc__, argv=self.split_arguments(arguments), version=COMPARE_CMD_VERSION)

        # get a list of unique, valid, friends
        friends = list(filter(lambda f: f.name in opt["--friend"], client_provider.get_friends(force=opt["--force"])))
        game_list: Dict[str, FriendGameComparison] = {}

        # build up a list of games, and add friends who own each game as attributes of each game
        for friend in friends:

            friend_games = client_provider.get_games(user_id=friend.user_id, force=opt["--force"])

            for game in friend_games:
                if game.appid in game_list:
                    game_list[game.appid].owned_by.append(friend)
                else:
                    game_list[game.appid] = FriendGameComparison(owned_by=[friend], game=game)

        # create output lists, by number of friends who own each game
        # output the list of games owned by everyone first.

        # create the title row and pre-populate each list of games by number of owners...
        title_row = ["Game"]
        games_by_num_owners: List[List[Any]] = []
        for friend in friends:
            games_by_num_owners.append([])
            title_row.append(f'"{friend.name}"')
        title_row.append("Notes")

        skip_partial_owned = opt["--all-owned-games"]

        # inspect each game and convert to a linear row of data
        for key in game_list.keys():

            # only bother to record partially-owned games if we need to
            if skip_partial_owned and len(game_list[key].owned_by) != len(friends):
                continue

            current_game = game_list[key]
            game_row: List[Any] = [f'"{current_game.game.name}"']  # add quotes to satisfy CSV nonsense

            # order is important, each entry is either True or False
            for friend in friends:
                game_row.append(friend in current_game.owned_by)

            # append this to the right number-owned games list
            games_by_num_owners[len(game_list[key].owned_by) - 1].append(game_row)

        gol: List[List[str]] = [[""], [f"compare: Generated on {datetime.datetime.now()}"]]
        # output a summary
        for index in reversed(range(len(friends))):
            if len(games_by_num_owners[index]) > 0:
                gol.append([f"OWNED BY {index+1} FRIENDS (count={len(games_by_num_owners[index])})"])

        gol.append([""])
        # start building the output.
        gol.extend([title_row])

        # combine the lists
        for index in reversed(range(len(friends))):
            if len(games_by_num_owners[index]) > 0:
                gol.extend(games_by_num_owners[index])

        return [",".join(str(item) for item in row) for row in gol]
