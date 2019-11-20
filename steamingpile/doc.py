"""steamingpile

Compare the games you own against those of your Steam connected friends. Various different
commands are available, each caching their results so that every subsequent run can be done
without reaching out to any game client/game launcher API. 

Usage:
  steamingpile.py --help
  steamingpile.py --version
  steamingpile.py [--user-steam-api-dev-key=KEY]
                  [--force]
                  [--output-file=PATH] [--output-format=FMT]
                  [--user=USER] [--passwd=PWD]
                  <cmd> [<args>...]

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
  -f --output-format=FMT            Output file format. You can specify one of json, text, or csv. [Default: csv]
  --user-steam-api-dev-key=<key>    Your own personal Steam API dev key. See description below in
                                    Environment Variables/Dotfiles sections.
  <cmd>                             Run this command and exit. ()
  <args>                            Arguments to pass to the command being run, see 'help <cmd>' for details.

Commonly used commands:
    help [CMD]    Print all available commands. If a CMD is specified print the help for that command.
    configure     Change configuration of the app during runtime.
    exit          Exit interactive mode and the program.
    games         Get a list of all games owned by the logged in user.
    friends       Get a list of all Steam friends for the logged in user.
    compare       Get a list of games you share with friend(s). Specify

Environment Variables:
  USER_STEAM_API_DEV_KEY:   Contains a string value that is the steam API key for the user
                            running the application. Some of the internal calls made require a
                            Steam API key. Get one here https://steamcommunity.com/dev/apikey.

Files:
  ~/.steamingpile/.user_steam_api_dev_key: Contains a string value that is the steam API key for 
                              the user running the application. Some of the internal calls made
                              require a Steam API key. Get one here:
                              https://steamcommunity.com/dev/apikey

  ~/.steamingpile/*.cache     Files that store results pertaining to commands issued in a prior
                              run of the program. Use the --force switch to override use of these
                              cache files. It is safe to delete these files before running the
                              program. 
"""  # noqa501
