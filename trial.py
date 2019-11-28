""" trial

Usage:
    trial.py [--force] <command> [<args>...]

Options:
    -F --force              Force the query, don't use the local cache.

Commands that you can use are:

    help CMD            Get help on command CMD.
    compare             Compare games between friends.
    games               Get a list of games for yourself or for a friend.
    friends             Get a list of the friends you know.
"""  # nofa

from typing import List
import docopt  # type: ignore

import trial_compare


def show_help(args: List[str]):
    print(f"Show help for command '{args[0]}")


def print_cmd_args(cmd: str, args: List[str], force: bool):
    print(f"{cmd} command")
    print("")
    print("Arguments sent in:")
    for arg in args:
        print(f"  {arg}")


def do_compare(args: List[str], force: bool):
    print_cmd_args("Compare", args, force)
    print("")
    print("")
    trial_compare.do_compare(args, force)


def do_games(args: List[str], force: bool):
    print_cmd_args("Compare", args, force)


def do_friends(args: List[str], force: bool):
    print_cmd_args("Compare", args, force)


if __name__ == "__main__":
    opt = docopt.docopt(__doc__, options_first=True)

    cmd = opt["<command>"]
    args = opt["<args>"]
    force = "--force" in opt and opt["--force"]

    if cmd == "help":
        show_help(args)
    elif cmd == "compare":
        do_compare(args, force)
    elif cmd == "games":
        do_games(args, force)
    elif cmd == "friends":
        do_friends(args, force)
    else:
        print(f"Unknown command '{cmd}'. Use 'help' command to see options available.")
