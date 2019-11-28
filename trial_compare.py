""" Print out a list of all the games owned by the specified user, or of all
the games owned by the currently logged in user. The user can be specified
by their steam ID or by their steam user name.

Usage:
    compare --friend=USER ... [--force] [--all-owned-games]

Options:
    -f --friend=USER        Specify the user name of the game client friend to compare the games with,
                            multiple separated by commas.
    -a --all-owned-games    Only output games that are owned by every friend specified.
"""  # noqa
from typing import List

import docopt  # type: ignore


COMPARE_VER = 0.1


def do_compare(args: List[str], force: bool) -> List[str]:
    opts = docopt.docopt(__doc__, argv=args, help=False, version=COMPARE_VER)
    print("Compare command")
    print("")
    print("Arguments:")
    print(opts)
    print("")
    print("--")
    print("")
    return ["booyeah"]
