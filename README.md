# Steamingpile
## An app to help you and your Steam friends determine what game to play.


# How to build
Python app, so there isn't really any need to build! 
You will need a Steam app id though, you can get one here: https://steamcommunity.com/login/home/?goto=%2Fdev%2Fapikey
Once you have this number, you can either:
- Specify the value in the command line `--steam-dev-api-key=<your_key>`.
- Set it into an environment variable when you run the app called `USER_STEAM_API_DEV_KEY`.
- Write it to a file in the root folder of this repo before you run it. Call the file `.user_steam_api_dev_key` 
  and copy your key to the file without quotation marks and on the first line of the file. The rest of the file
  will be ignored.


# How to use
Install the latest stable version of Python
- [Windows] Go to https://python.org and download the latest version of Python and run the installer.
- [Linux] Use your distros built-in package manager to install the latest version of Python.
- [MacOS] Go to https://python.org and download the latest version of Python and run the installer.
  - _Optionally_: Use `brew install python3` once you've installed and configured [`brew`](https://brew.sh)

# How to contribute

> **Very important note!** Since this is mainly a learning repo used by the original author to learn and play with Python.

1. Clone the repo
2. Create your own feature branch off of master
3. Create your local Python virtual environment 
  - `python -m venv .venv`
  - Activate your virtual env `source .venv/bin/activate`
  - Update `pip` in your venv `python -m pip install -U pip`
4. Install the required packages into your venv `python -m pip install -r requirements.txt`
5. **Important**: Ensure tests all run and pass before you start!
6. Create a feature branch to work in `git checkout -b my_feature_branch_name`
7. Do your work
8. Ensure tests pass (you did remember to ensure tests passed to begin with right?)
9. Push your feature branch `git push -u origin my_feature_branch_name`
10. Create a PR against my master via Github.

# TODO:
- [x] Refactor the POC script `testsp.py` into a proper _'Pythonic'_ layout.
- [x] Remove the author's Steam app-key and allow others to set it via the build/package commands.
- [ ] Pull out the various major systems used in the app and recreate them as classes.
- [ ] Add tests using pytest or similar.
- [ ] Create Github actions to test the code whenever a PR is created.
- [ ] Mock out the Steam Web API such that tests can be run without having to incure Steam calls.
- [ ] Add game types to the list of users games so they can sort out co-op, multiplayer, split-screen, and single-player games.
