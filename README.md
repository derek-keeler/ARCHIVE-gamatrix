# Gamatrix

![Build Status Badge](https://github.com/d3r3kk/gamatrix/workflows/CI/badge.svg)

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
git clone https://github.com/d3r3kk/gamatrix
cd gamatrix
echo "my_personal_steam_web_api_key" > .user_steam_api_dev_key # get key here: https://steamcommunity.com/dev/apikey
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
pytest # This is optional, if you are going to do some development...
python -m gamatrix
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

`gamatrix` is a Python app, so instead of building you set up an environment. Our suggestion is that you create a
_virtual environment_ using the built-in Python library `venv` to do so. Instructions to get a `venv` up and running:

### Windows Prep

1. Open a Powershell window.
    - *Start->Powershell*
1. Navigate to a folder where you will run `gamatrix` from.
    - `cd ~/Documents`
1. Clone the repo.
    - `git clone https://github.com/d3r3kk/gamatrix`
1. Create a virtual environment in the repo and activate it.
    - `cd gamatrix`
    - `py -3.8 -m venv .venv --prompt "gamatrix"`
      - (alternatively, use `py -3.7 ...` for Python version 3.7)
    - `.venv/Scripts/Activate.ps1`
      - If you get errors stating that the `...Execution policy is Restricted...`, see [Troubleshooting](#troubleshooting).

### Linux/Mac Prep

1. Open a terminal.
    - *Meta->Terminal*
1. Navigate to a folder where you will run `gamatrix` from.
    - `cd ~/`
1. Clone the repo.
    - `git clone https://github.com/d3r3kk/gamatrix`
1. Create a virtual environment in the repo and activate it.
    - `cd gamatrix`
    - `python3 -m venv .venv --prompt "gamatrix"`
    - `. .venv/bin/activate`

### Finish up, all platforms

1. Install the dependencies for the application into the venv.
    - `python -m pip install --upgrade pip`
    - `python -m pip install -r requirements.txt`
1. Make your API key available to the application.
    1. `mkdir -p ~/.gamatrix`
    1. `cat 'your_api_key_here' > ~/.gamatrix/.user_steam_api_dev_key
    - Note that you can set this as an environment variable called `USER_STEAM_API_DEV_KEY` or supply
      it on the command line.

## How to Run

Once you are all setup and have the [prerequisites](#prerequisites) and [preparation](#preparation) complete, you can
now run the application.

1. Open your shell of choice.
1. Navigate to the `gamatrix` folder. (Note this is the root-folder you cloned to in Git, **_not_** the `gamatrix/gamatrix` folder within the repo).
1. Activate the Python venv.
1. Run the application with the `--help` flag to see what options/commands are available.
    - `python -m gamatrix --help`
1. Run the application.
    - Show off all your connected friends:
    - `python -m gamatrix friends`

### A Note About Cache

The application tries to minimize the amount of times it will reach out to the game client service. To achieve this,
the results from the basic queries about friends and games are cached between runs. The caches are stored under the
users home directory, under a folder called `.gamatrix/cache`. The files located there can be removed at any time,
and can be ignored during runtime by using the `--force` command line option.

Users can look through these cache files using Python, as they are simply _pickled objects_ with a fairly basic schema.

### Examples

Show friends:

`python -m gamatrix --user=<username> --passwd='<password>' friends`

Compare games with `friend 1` and `friend_2`:

`python -m gamatrix --user=<username> --passwd='<password>' compare --friend="<friend 1>" --friend=<friend_2>`

## How to Contribute

Quick setup steps...

1. Clone the repo.

    - `git clone https://github.com/d3r3kk/gamatrix`

1. Create your local Python virtual environment and install requirements.txt.

    - `python -m venv .venv`
    - `. .venv/bin/activate`
    - `python -m pip install -U pip`
    - `python -m pip install -r requirements.txt`

1. **Important**: Ensure tests all run and pass before you start!

    - `pytest`

1. Create your own feature branch off of master.

    - `git checkout -b my_feature master`

1. Do your work.
1. Ensure tests pass.

    - `pytest`

1. Push your feature branch.

    - `git push --set-upstream origin my_feature`

1. Create a PR against `master` via Github.

---

> NOTE: If you need to update `requirements.txt`

Please don't update that file directly. Add your package requirement to `requirements.in` and use `pip-tools`
to update the files and pin all dependencies.

```pwsh
python -m pip install pip-tools
pip-compile
python -m pip install -r requirements.txt
```
---

## Code of Conduct

Basic Premise: _Be excellent to each other_.

In general, this means that everyone is expected to be **open**, **considerate**, and
**respectful**, of others no matter what their perspective is within this project.

## Troubleshooting

### Windows Problems

---

**Issue:** The C++ Build Tools aren't available.

Error message occurs during `python -m pip install -r requirements.txt` stage.

Error message ends with:
`"distutils.errors.DistutilsPlatformError: Microsoft Visual C++ 14.0 is required. Get it with "Microsoft Visual C++ Build Tools": https://visualstudio.microsoft.com/downloads/"`

**Solution:** Install the Microsoft build tools by installing the Visual Studio Community Edition from the link provided. Be certain to install the `MSVC v[VER] - VS 20xx C++ x64/x86 build tools (vMAJ.MIN)` are selected in "Individual Components" within the Visual Studio installer. You can install the "Desctop development with C++" workload to ensure you get everything. Alternatively, install only the "C++ Build Tools" workload for the latest Visual Studio (currently [you can find them for Visual Studio 2019 here](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019)).

---

**Issue:** The Powershell `Activate.ps1` script raises permissions errors.

Error message occurs during activation of the Python environment `.venv\Scripts\Activate.ps1`.

Error message is:

```pwsh
.\.venv\Scripts\Activate.ps1 : File C:\path\to\gamatrix\.venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system. For more information, see about_Execution_Policies at https://go.microsoft.com/fwlink/?LinkID=135170.
At line:1 char:1
+ .\.venv\Scripts\Activate.ps1
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
+ CategoryInfo          : SecurityError: (:) [], PSSecurityException
+ FullyQualifiedErrorId : UnauthorizedAccess
```

**Solution:** The Powershell access is set to something _less than_ `RemoteSigned`. Change the execution
policy to `RemoteSigned`.

```pwsh
 Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
 ```

---
