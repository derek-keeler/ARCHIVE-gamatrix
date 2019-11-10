# Steamingpile

## An app to help you and your Steam friends determine what game to play.

### How to build

Python app, so there isn't really any need to build!
You will need a Steam app id though, [you can get one by clicking here](https://steamcommunity.com/login/home/?goto=%2Fdev%2Fapikey).
Once you have this number, you can either:

- Specify the value in the command line `--steam-dev-api-key=<your_key>`.
- Set it into an environment variable when you run the app called `USER_STEAM_API_DEV_KEY`.
- Write it to a file in the root folder of this repo before you run it. Call the file `.user_steam_api_dev_key`
  and copy your key to the file without quotation marks and on the first line of the file. The rest of the file
  will be ignored.

```powershell
py -3.7 -m venv .venv
.venv/Scripts/Activate.ps1
python -m pip install -U pip
python -m pip install -r requirements.txt

# if you want to update the dependencies in `requirements.in`:
python -m pip install pip-tools
pip-compile
python -m pip install -r requirements.txt
```

### How to run tests

```bash
python -m pytest tests -W ignore::DeprecationWarning
```

### How to use

Install the latest stable version of Python

- [Windows] Go to https://python.org and download the latest version of Python and run the installer.
- [Linux] Use your distros built-in package manager to install the latest version of Python.
- [MacOS] Go to https://python.org and download the latest version of Python and run the installer.
  - _Optionally_: Use `brew install python3` once you've installed and configured [`brew`](https://brew.sh)

### How to contribute

> **Very important note!** Since this is mainly a learning repo used by the original author to learn and play with Python, any contributions may not be accepted but will certainly be _appreciated_ to help in the learning process!

1. Clone the repo. (`git clone https://github.com/d3r3kk/steamingpile`)
1. Enter the cloned repo directory. (`cd steamingpile`)
1. Create your own feature branch off of master. (`git checkout -b my_feature_branch_name_here`)
1. Create your local Python virtual environment. (`python -m venv .venv`)
    - Activate your virtual env. (`source .venv/bin/activate`)
    - Update `pip` in your venv. (`python -m pip install -U pip`)
1. Install the required packages into your venv. (`python -m pip install -r requirements.txt`)
1. **Important**: Ensure tests all run and pass before you start!
1. Create a feature branch to work in. (`git checkout -b my_feature_branch_name`)
1. Do your work!
1. Ensure tests pass (you did remember to ensure tests passed to begin with right?) (`python -m pytest -W ignore::DeprecationWarning`)
1. Push your feature branch. (`git push -u origin my_feature_branch_name`)
1. Create a PR against the master via Github.

---

#### TODO

- [x] Refactor the POC script `testsp.py` into a proper _'Pythonic'_ layout.
- [x] Remove the author's Steam app-key and allow others to set it via the build/package commands.
- [x] Pull out the various major systems used in the app and recreate them as classes.
- [x] Add tests using pytest or similar.
- [ ] Create Github actions to test the code whenever a PR is created.
- [x] Mock out the Steam Web API such that tests can be run without having to incure Steam calls.
- [ ] Add game types to the list of users games so they can sort out co-op, multiplayer, split-screen, and single-player games.

