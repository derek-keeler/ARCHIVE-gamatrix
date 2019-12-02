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
  --user=<usr>                      Game launcher client user name.
  --passwd=<pwd>                    Game launcher client password.
  <cmd>                             Run this command and exit. ()
  <args>                            Arguments to pass to the command being run, see 'help <cmd>' for details.
  --user-steam-api-dev-key=<key>    Your own personal Steam API dev key. See description below in
                                    Environment Variables/Dotfiles sections.

Commonly used commands:
    help [CMD]    Print all available commands. If a CMD is specified print the help for that command.
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
