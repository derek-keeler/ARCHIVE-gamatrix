"""Test the configuration object and command-line options."""
import pathlib
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


def test_stdout_enable():
    """Is stdout enabled by default in the config object?"""
    opts = docopt.docopt(appdoc.__doc__, version="0.0.0+test_run_only", argv=[])
    cfg = config.SteamingPileConfig(opts)
    assert cfg.enable_stdout


def test_stdout_disable():
    """Does disabling stdout work in the config object?"""
    opts = docopt.docopt(appdoc.__doc__, version="0.0.0+test_run_only", argv=["--quiet"])
    cfg = config.SteamingPileConfig(opts)
    assert not cfg.enable_stdout


def test_output_file_unset_by_default():
    """Is the output file by default unset in the config object?"""
    opts = docopt.docopt(appdoc.__doc__, version="0.0.0+test_run_only", argv=[])
    cfg = config.SteamingPileConfig(opts)
    assert cfg.output_file is None


def test_output_file_set_valid():
    """Given a valid file path, is it set into the config object?"""
    test_file_uri = pathlib.Path(f"{__file__}.test").as_posix()
    test_switch = f"--output-file={test_file_uri}"
    opts = docopt.docopt(appdoc.__doc__, version="0.0.0+test_run_only", argv=[test_switch])
    cfg = config.SteamingPileConfig(opts)
    assert cfg.output_file.as_posix() == test_file_uri


def test_output_file_handles_bad_characters():
    """Given an invalid file path, is the config object still valid (even though the path will never work)?"""
    bad_filename = "test&invalid\\why-would-anyone-do-this^file,no?use"
    test_switch = f"--output-file={bad_filename}"
    opts = docopt.docopt(appdoc.__doc__, version="0.0.0+test_run_only", argv=[test_switch])
    cfg = config.SteamingPileConfig(opts)
    assert f"{cfg.output_file}" == bad_filename


def test_output_file_format_default():
    """Default file format is csv."""
    opts = docopt.docopt(appdoc.__doc__, version="0.0.0+test_run_only", argv=[])
    cfg = config.SteamingPileConfig(opts)
    assert cfg.output_format == "csv"


def test_output_file_format_text():
    """Setting the output file format to text works."""
    opts = docopt.docopt(appdoc.__doc__, version="0.0.0+test_run_only", argv=["--output-format=TEXT"])
    cfg = config.SteamingPileConfig(opts)
    assert cfg.output_format == "text"


def test_output_file_format_json():
    """Setting the output file format to json works."""
    opts = docopt.docopt(appdoc.__doc__, version="0.0.0+test_run_only", argv=["--output-format=jsOn"])
    cfg = config.SteamingPileConfig(opts)
    assert cfg.output_format == "json"


def test_output_file_format_csv():
    """Setting the output file format to csv works."""
    opts = docopt.docopt(appdoc.__doc__, version="0.0.0+test_run_only", argv=["--output-format=csv"])
    cfg = config.SteamingPileConfig(opts)
    assert cfg.output_format == "csv"


def test_output_file_format_invalid():
    """Setting the output file format to an invalid type is handled correctly."""
    opts = docopt.docopt(appdoc.__doc__, version="0.0.0+test_run_only", argv=["--output-format=nothing"])
    cfg = config.SteamingPileConfig(opts)
    assert cfg.output_format == "csv"
