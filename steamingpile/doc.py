"""steamingpile

Compare the games you own against those of your Steam connected friends. The default is to load the
app and execute in interactive mode, but commands can also be specified on the command line to just
produce output and exit.

Usage:
  steamingpile.py
  steamingpile.py (-h | --help)
  steamingpile.py --version
  steamingpile.py [--user=<usr>] [--passwd=<pwd>] [--command=<cmd>] [--quiet] [--user-steam-api-dev-key=<key>]

Options:
  -h --help                         Show this screen.
  -v --version                      Show version.
  -u --user=<usr>                   Steam user name.
  -p --passwd=<pwd>                 Steam user password.
  -c --command=<cmd>                Run this command and exit. For commands that take > 1 arg
                                    enclose the command and args in quotes.
  -q --quiet                        Do not send output to stdout from any commands. Useful when used with --output-file.
  -o --output-file=PATH             Send all command output to the file specified in PATH. If it exist, it will be
                                    overwritten.
  -f --output-format=FRMT           Output file format. You can specify one of [JSON, TEXT, or CSV], default is TEXT.
  --user-steam-api-dev-key=<key>    Your own personal Steam API dev key. See description below in
                                    Environment Variables/Dotfiles sections.

Available Commands:
    help                        Print the available commands.
    exit                        Exit interactive mode and the program.
    games                       Get a list of all games owned by the logged in user.
    friends                     Get a list of all Steam friends for the logged in user.
    compare --friend=USR ...    Get a list of games you share with friend(s). Specify
                                --friend=USR multiple times.

Environment Variables:
  USER_STEAM_API_DEV_KEY:   Contains a string value that is the steam API key for the user
                            running the application. Some of the internal calls made require a
                            Steam API key. Get one here https://steamcommunity.com/dev/apikey.

Dotfiles:
  .user_steam_api_dev_key:  Contains a string value that is the steam API key for the user
                            running the application. Some of the internal calls made require a
                            Steam API key. Get one here https://steamcommunity.com/dev/apikey.
"""  # noqa501
