"""Test the configuration object and command-line options."""
import unittest

import docopt

from steamingpile import steaming_pile_config
from steamingpile import __main__ as app_main

TEST_RUN_API_KEY = "12345678901234567890"


def test_apikey():
    """Does the apikey get resolved from the command line switch."""
    opts = docopt.docopt(
        app_main.__doc__, version="0.0.0+test_run_only", argv=[f"--user-steam-api-dev-key={TEST_RUN_API_KEY}"]
    )
    config = steaming_pile_config.SteamingPileConfig(opts)
    assert config.api_key()
    assert config.api_key() == TEST_RUN_API_KEY


def test_apikey_file(monkeypatch):
    """Does the apikey get resolved from the dotfile at the root of the app?"""
    from unittest.mock import patch, mock_open

    with patch("pathlib.Path.is_file", unittest.mock.Mock(return_value=True)):
        with patch("builtins.open", mock_open(read_data=TEST_RUN_API_KEY)):
            opts = docopt.docopt(app_main.__doc__, version="0.0.0+test_run_only", argv=[])
            config = steaming_pile_config.SteamingPileConfig(opts)
            assert config.api_key() is not None
            assert config.api_key() == TEST_RUN_API_KEY


def test_apikey_env(monkeypatch):
    """Does the apikey get resolved from the environment?"""
    monkeypatch.setenv("USER_STEAM_API_DEV_KEY", TEST_RUN_API_KEY, prepend=False)
    opts = docopt.docopt(app_main.__doc__, version="0.0.0+test_run_only", argv=[])
    config = steaming_pile_config.SteamingPileConfig(opts)
    assert config.api_key()
    assert config.api_key() == TEST_RUN_API_KEY
