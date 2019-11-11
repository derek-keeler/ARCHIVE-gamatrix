# Steamingpile

An app to help you and your Steam friends determine what game to play.

## Contents

- [Quick Setup](#quick-setup-for-the-mildly-impatient)
- [Prerequisites](#prerequisites)
- [Preparation](#preparation)
- [How to Run](#how-to-run)
- [How to Contribute](#how-to-contribute)

---

## Quick Setup for the Mildly Impatient

> _Step #1: **All platforms**_

```bash
git clone https://github.com/d3r3kk/steamingpile
cd steamingpile
```

> _Step #2 Option A: **Windows Powershell**_

```pwsh
py -3.8 -m venv .venv
.venv/Scripts/Activate.ps1
```

> _Step #2 Option B: **MacOS/Linux Bash**_

```bash
python3 -m venv .venv
. .venv/bin/activate
```

> _Step #3: **All platforms**_

```bash
python -m pip install -U pip
python -m pip install -r requirements.txt
python -m steamingpile
```

---

## Prerequisites

- Python 3.7 or higher installed (see [Python.org for downloads](https://www.python.org/downloads/)).
  - [Windows][MacOS] Go to [Python.org website](https://python.org) and download the latest version of Python and run the installer.
    - _[MacOS] Optional_ Use `brew install python3` once you've installed and configured [`brew`](https://brew.sh).
  - [Linux] Use your distros built-in package manager to install the latest version of Python.
    - `sudo apt-get install python3 python3-pip python3-venv`
- The Git client installed on your system and accessible via PATH.
  - [Windows][MacOS] [Get the latest installer from the Git site](https://git-scm.org).
    - _[MacOS] _Optional_ Use `brew install git`
  - [Linux] use your distros built-in package manager to install the latest version available.
    - `sudo apt-get install git`
- A Steam account, and at least one friend! (go to [Steam online to sign up](https://steampowered.com/)).
- A Steam Web API Key (see [Steam community Web API Page for details](https://steamcommunity.com/dev/apikey)).

## Preparation

`steamingpile` is a Python app, so instead of building you set up an environment. Our suggestion is that you create a
_virtual environment_ using the built-in Python library `venv` to do so. Instructions to get a `venv` up and running:

### Windows

1. Open a Powershell window.
    - *Start->Powershell*
1. Navigate to a folder where you will run `steamingpile` from.
    - `cd ~/Documents`
1. Clone the repo.
    - `git clone https://github.com/d3r3kk/steamingpile`
1. Create a virtual environment in the repo and activate it.
    - `cd steamingpile`
    - `py -3.8 -m venv .venv --prompt "steamingpile"`
      - (alternatively, use `py -3.7 ...` for Python version 3.7)
    - `.venv/Scripts/Activate.ps1`

### Linux/Mac

1. Open a terminal.
    - *Meta->Terminal*
1. Navigate to a folder where you will run `steamingpile` from.
    - `cd ~/`
1. Clone the repo.
    - `git clone https://github.com/d3r3kk/steamingpile`
1. Create a virtual environment in the repo and activate it.
    - `cd steamingpile`
    - `python3 -m venv .venv --prompt "steamingpile"`
    - `. .venv/bin/activate`

### Finish up, all platforms

1. Install the dependencies for the application into the venv.
    - `python -m pip install --upgrade pip`
    - `python -m pip install -r requirements.txt`
1. Make your API key available to the application.
    - `cat 'your_api_key_here' > .user_steam_api_dev_key
    - Note that you can set this as an environment variable called `USER_STEAM_API_DEV_KEY` or supply
      it on the command line.

## How to Run

Once you are all setup and have the [prerequisites](#prerequisites) and [preparation](#preparation) complete, you can
now run the application.

1. Open your shell of choice.
1. Navigate to the `steamingpile` folder. (Note this is the root-folder you cloned to in Git, **_not_** the `steamingpile/steamingpile` folder within the repo).
1. Activate the Python venv.
1. Run the application with the `--help` flag to see what options/commands are available.
    - `python -m steamingpile --help`
1. Run the application.
    - `python -m steamingpile`

## How to Contribute

Quick setup steps...

1. Clone the repo.
1. Create your own feature branch off of master.
1. Create your local Python virtual environment and install requirements.txt.
1. **Important**: Ensure tests all run and pass before you start!
1. Create a feature branch to work in.
1. Do your work.
1. Ensure tests pass.
1. Push your feature branch.
1. Create a PR against `master` via Github.

> NOTE: If you need to update `requirements.txt`

Please don't update that file directly. Add your package requirement to `requirements.in` and use `pip-tools`
to update the files and pin all dependencies.

```pwsh
python -m pip install pip-tools
pip-compile
python -m pip install -r requirements.txt
```

## Code of Conduct

Basic Premise: _Be excellent to each other_.

In general, this means that everyone is expected to be **open**, **considerate**, and
**respectful**, of others no matter what their perspective is within this project.
