"""steamingpile

Compare the games you own against those of your Steam connected friends.
Default is to load the app and execute in interactive mode, but commands
can also be specified on the command line to just produce output and exit.

Usage:
  steamingpile.py
  steamingpile.py (-h | --help)
  steamingpile.py --version
  steamingpile.py [--user=<usr>] [--passwd=<pwd>] [--command=<cmd>] [--output-format=<fmt>] [--output-file=<file>]

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
  --user-steam-api-dev-key=<key>    Your own personal Steam API dev key. See description below in
                                    Environment Variables/Dotfiles sections.

Available Commands:
    help                    Print the available commands.
    exit                    Exit interactive mode and the program.
    game <gid>              Get detailed information on a game based on its game_id (name, or app-id).
    games                   Get a list of all games owned by the logged in user.
    friend <fid>            Get detailed information on a friend based on their steam name or id.
    friends                 Get a list of all Steam friends for the logged in user.
    friend <f>              Get a list of the games for friend named <f>.
    compare <f>[,<f>[,...]] Get a list of games you share with friend <f>.
                            Where <f> can be the friend's name or multiple friend
                            names separated by commas.

Environment Variables:
  USER_STEAM_API_DEV_KEY:   Contains a string value that is the steam API key for the user
                            running the application. Some of the internal calls made require a
                            Steam API key. Get one here https://steamcommunity.com/dev/apikey.

Dotfiles:
  .user_steam_api_dev_key:  Contains a string value that is the steam API key for the user
                            running the application. Some of the internal calls made require a
                            Steam API key. Get one here https://steamcommunity.com/dev/apikey.
"""

import docopt

from steamingpile.steaming_pile_config import SteamingPileConfig
from steamingpile.steaming_pile import SteamingPile

STEAMINGPILE_VERSION = 0.1

if __name__ == "__main__":
    opt = docopt.docopt(__doc__, version=STEAMINGPILE_VERSION)

    config = SteamingPileConfig(opt)
    sp = SteamingPile(config)
    sp.run()
