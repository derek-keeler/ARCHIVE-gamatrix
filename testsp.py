"""steamingpile

Compare the games you own against those of your Steam connected friends.
Default is to load the app and execute in interactive mode, but commands
can also be specified on the command line to just produce output and exit.

Usage:
  steamingpile.py
  steamingpile.py (-h | --help)
  steamingpile.py --version
  steamingpile.py [--user-steam-api-dev-key=<key>]
  steamingpile.py [--user=<usr>] [--passwd=<pwd>]
  steamingpile.py [--command=<cmd>] [--output-format=<fmt>] [--output-file=<file>]

Options:
  -h --help                         Show this screen.
  --version                         Show version.
  --user=<usr>                      Steam user name.
  --passwd=<pwd>                    Steam user password.
  --command=<cmd>                   Run this command and exit. For commands that take > 1 arg
                                    enclose the command and args in quotes.
  --output-format=<fmt>             Specify the output format <fmt> to output from commands,
                                    defaults to plain text.
  --output-file=<file>              Specify an output file <file> to write into, instead of
                                    writing to stdout.
  --user-steam-api-dev-key=<key>    Your own personal Steam API dev key. See README.md for details.

Available Interactive Commands:
    help                    Print the available commands.
    exit                    Exit interactive mode and the program.
    games                   Get a list of all owned games of the logged in user.
    friends                 Get a list of all Steam friends for the logged in user.
    friend <f>              Get a list of the games for friend named <f>.
    compare <f>[,<f>[,...]] Get a list of games you share with friend <f>.
                            Where <f> can be the friend's name or multiple friend
                            names separated by commas.

Environment Variables:
"""

from __future__ import print_function

from contextlib import redirect_stdout

import docopt
import os
from pathlib import Path

from steam.client import SteamClient
from steam.client.user import SteamUser

# from steam.client.builtins.friends import SteamFriendlist
# from steam.client.builtins.apps import Apps
from steam.enums import EResult
from steam.webapi import WebAPI

STEAMINGPILE_VERSION = "0.1"
OUTPUT_FORMATS = ["text", "json", "csv"]


def login_with_2fa(user: str = None, passwd: str = None) -> SteamClient:
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


def accept_interactive_commands(client: SteamClient, api_key: str, output_format: str = OUTPUT_FORMATS[0]):
    """Wait for textual commands to respond to."""

    keep_accepting_commands = True
    cmd = input("steamingpile cmd: ")

    while keep_accepting_commands:

        if cmd.casefold() == "exit":
            logout_from_steam(client)
            keep_accepting_commands = False
        else:
            run_command(client=client, command=cmd, api_key=api_key, output_format=output_format)

        if keep_accepting_commands:
            cmd = input("steamingpile cmd: ")


def print_out_games_list(games_lists: dict, output_file: str = None, output_format: str = OUTPUT_FORMATS[0]):
    """Print out a list of games and IDs."""
    if output_file is not None:
        with open(output_file, "w") as output_stream:
            with redirect_stdout(output_stream):
                do_print_out_games(games_lists, output_format)

    else:
        do_print_out_games(games_lists, output_format)


def do_print_out_games(games_lists: dict, output_format: str):

    if output_format == "text":
        print("Games List:")
    elif output_format == "csv":
        print("game_id,game_name")
    elif output_format == "json":
        print("{" "games" ":")
        print("  [")

    for game_id in games_lists.keys():
        game_info = {"id": game_id, "name": games_lists[game_id]["name"]}
        if output_format == "text":
            print("%(id)d: %(name)s" % game_info)
        elif output_format == "csv":
            print('%(id)d, "%(name)s"' % game_info)
        elif output_format == "json":
            print('     "id": %(id)d' % game_info)
            print('     "name": "%(name)s"' % game_info)

    if output_format == "json":
        print("  ]")
        print("}")

    print()


def get_steam_user_by_steamid(client: SteamClient, steamid: int) -> SteamUser:
    """Given a steam id, return the SteamUser for that id from the logged in user's friend list."""

    friend_user = None

    for friend in client.friends:
        if int("%(sid)s" % {"sid": friend.steam_id}, 10) == steamid:
            friend_user = friend
            break

        return friend_user


def get_steam_user_by_name(client: SteamClient, name: str) -> SteamUser:
    """Given a name, return the SteamUser for that name from the logged in user's friend list."""

    friend_user = None

    for friend in client.friends:
        if friend.name == name:
            friend_user = friend

    return friend_user


def intersect_games_lists(game_lists: dict) -> dict:
    """Given 2 or more game lists, intersect them and return the intersection."""
    all_games = dict(game for dictionary in game_lists for game in dictionary.items())

    games_owned_per_list = [set(owned_games.keys()) for owned_games in game_lists]
    shared_game_ids = set.intersection(*games_owned_per_list)

    shared_games = {game_id: all_games[game_id] for game_id in shared_game_ids}

    return shared_games


def get_games_for_user(client: SteamClient, user: SteamUser, api_key: str) -> dict:
    """Use a steam client instance to get a list of owned games for a user."""
    api = WebAPI(key=api_key)
    response = api.call(
        "IPlayerService.GetOwnedGames",
        key=api_key,
        steamid=user.steam_id,
        include_appinfo=True,
        include_played_free_games=False,
        appids_filter=None,
    )
    r = response["response"]
    games = {g["appid"]: {"name": g["name"]} for g in r["games"]}

    return games


def logout_from_steam(client: SteamClient):
    """Just logout and be done with it."""

    client.logout()


def print_out_friends(friends: [SteamUser], output_file: str = None, output_format: str = OUTPUT_FORMATS[0]):
    """Print out a list of SteamUser friends in the output format specified."""
    if output_file is not None:
        with open(output_file, "w", encoding="utf8") as output_stream:
            with redirect_stdout(output_stream):
                do_print_out_friends(friends, output_format)

    else:
        do_print_out_friends(friends, output_format)


def do_print_out_friends(friends: [SteamUser], output_format: str):

    if output_format == "text":
        print("Friends:")
        for friend in friends:
            print(
                "    [name]: %(friend_name)s [steam_id]: %(friend_id)s"
                % {"friend_name": friend.name, "friend_id": friend.steam_id}
            )
    elif output_format == "csv":
        print("name,steam_id")
        for friend in friends:
            print("%(friend_name)s,%(friend_id)s" % {"friend_name": friend.name, "friend_id": friend.steam_id})
    elif output_format == "json":
        comma = ""
        print("{" "friends" ":")
        print("  [")
        for friend in friends:
            print("    {")
            print("       " "name" ": " "%(friend_name)s" "," % {"friend_name": friend.name})
            print("       " "steam_id" ": %(friend_id)s" % {"friend_id": friend.steam_id})
            print("    }%(comma)s" % {"comma": comma})
            comma = ","
        print("  ]")
        print("}")


def run_command(
    client: SteamClient, command: str, api_key: str, output_file: str = None, output_format: str = OUTPUT_FORMATS[0]
):
    """Run the command given."""

    raw_command = command
    cmd = command.casefold()

    if cmd == "help":
        print(__doc__)

    elif cmd == "exit":
        print("exit command should not be accessible here.")

    elif cmd == "friends":
        print_out_friends(friends=client.friends, output_file=output_file, output_format=output_format)

    elif cmd.startswith("friend"):
        name = raw_command.split(maxsplit=1)[1]
        friend_to_inspect = get_steam_user_by_name(client, name)
        if friend_to_inspect is None:
            friend_to_inspect = get_steam_user_by_steamid(client, int(name, 10))
        if friend_to_inspect is None:
            print("Could not find friend by name/id '%(fnm)s' or id %(fid)d" % {"fnm": name, "fid": int(name, 10)})
        else:
            games = get_games_for_user(client=client, user=friend_to_inspect, api_key=api_key)
            print_out_games_list(games_lists=games, output_file=output_file, output_format=output_format)

    elif cmd == "games":
        print("Show my own games list.")
        games = get_games_for_user(client=client, user=friend_to_inspect, api_key=api_key)
        print_out_games_list(games_lists=games, output_file=output_file, output_format=output_format)

    elif cmd.startswith("compare"):
        names = raw_command.split(maxsplit=1)[1].split(sep=",")

        print("Compare friend(s) %(friend_name)s games to mine." % {"friend_name": ",".join(names)})

        game_lists = [get_games_for_user(client=client, user=client.user, api_key=api_key)]
        for name in names:
            friend_to_inspect = get_steam_user_by_name(client, name)
            game_lists.append(get_games_for_user(client=client, user=friend_to_inspect, api_key=api_key))

        shared_games = intersect_games_lists(game_lists)
        print_out_games_list(games_lists=shared_games, output_file=output_file, output_format=output_format)

    elif len(cmd) > 0:
        print("Unknown command '%(command)s', use 'help'." % {"command": cmd})


def get_api_key(cmdline_key: str = None) -> str:
    """Return the API Dev key supplied by Steam to this user, or None."""

    if cmdline_key is None:
        # read the environment variable USER_STEAM_API_DEV_KEY
        cmdline_key = os.getenv("USER_STEAM_API_DEV_KEY")

    if cmdline_key is None:
        chk_file = Path(".user_steam_api_dev_key")
        if chk_file.is_file():
            with open(".user_steam_api_dev_key", "r") as f:
                cmdline_key = f.readline().strip()

    return cmdline_key


if __name__ == "__main__":
    opt = docopt.docopt(__doc__, version=STEAMINGPILE_VERSION)

    user = None
    pwd = None
    if "--user" in opt:
        user = opt["--user"]
    if "--passwd" in opt:
        pwd = opt["--passwd"]

    client = login_with_2fa(user=user, passwd=pwd)

    output_format = OUTPUT_FORMATS[0]
    if opt["--output-format"] in OUTPUT_FORMATS:
        output_format = opt["--output-format"]

    output_file = None
    if opt["--output-file"]:
        output_file = opt["--output-file"]

    api_key = get_api_key(opt["--user-steam-api-dev-key"])

    if opt["--command"]:
        command = opt["--command"].strip('"')
        run_command(
            client=client, command=command, api_key=api_key, output_format=output_format, output_file=output_file
        )
    else:
        accept_interactive_commands(client=client, api_key=api_key, output_format=output_format)

    logout_from_steam(client)
