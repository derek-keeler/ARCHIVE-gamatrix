"""Test the configuration object and command-line options."""
import unittest

import docopt  # type: ignore

from steamingpile import config
from steamingpile import doc as appdoc

TEST_RUN_API_KEY = "12345678901234567890"


def test_apikey():
    """Does the apikey get resolved from the command line switch."""
    opts = docopt.docopt(
        appdoc.__doc__, version="0.0.0+test_run_only", argv=["exit", f"--user-steam-api-dev-key={TEST_RUN_API_KEY}"]
    )
    cfg = config.SteamingPileConfig(opts)
    assert cfg.api_key()
    assert cfg.api_key() == TEST_RUN_API_KEY


def test_apikey_file(monkeypatch):
    """Does the apikey get resolved from the dotfile at the root of the app?"""
    from unittest.mock import patch, mock_open

    # For this process, ensure the env var is blanked out...
    monkeypatch.delenv("USER_STEAM_API_DEV_KEY", raising=False)
    with patch("pathlib.Path.is_file", unittest.mock.Mock(return_value=True)):
        with patch("builtins.open", mock_open(read_data=TEST_RUN_API_KEY)):
            opts = docopt.docopt(appdoc.__doc__, version="0.0.0+test_run_only", argv=["exit"])
            cfg = config.SteamingPileConfig(opts)
            assert cfg.api_key() is not None
            assert cfg.api_key() == TEST_RUN_API_KEY


def test_apikey_env(monkeypatch):
    """Does the apikey get resolved from the environment?"""
    monkeypatch.setenv("USER_STEAM_API_DEV_KEY", TEST_RUN_API_KEY, prepend=False)
    opts = docopt.docopt(appdoc.__doc__, version="0.0.0+test_run_only", argv=["exit"])
    cfg = config.SteamingPileConfig(opts)
    assert cfg.api_key()
    assert cfg.api_key() == TEST_RUN_API_KEY
