"""Test out the friends command."""

import docopt  # type: ignore

import gamatrix.commands as spcmd
import gamatrix.types as sptype

from . import utils


class TestFriendsCommand:

    # standard config not used for doing anything in this case.
    cfg = utils.Config()

    def test_friend_command_exists(self):
        """Friend command exists and is the right type."""
        friendcmd = spcmd.get_command("friends")
        assert friendcmd
        assert isinstance(friendcmd, spcmd.Friends)

    def test_friend_fails_bad_cmdline(self):
        """Friend command fails when given unknown commandline argument."""
        friendcmd = spcmd.get_command("friends")
        cli = utils.SettableClientProvider()
        cli.set_friends = [
            sptype.FriendInformation(name="d3r3kk", user_id="12345"),
            sptype.FriendInformation(name="other", user_id="67890"),
        ]
        self.cfg.command_args_val = ["--jibbity-flibbit"]
        try:
            friendcmd.run(self.cfg, cli)
            assert (
                "Argument parsing for friends command did not recognize bad input."
                == ""
            )
        except docopt.DocoptExit as e:
            assert "friends" in e.usage.lower()
            assert "usage" in e.usage.lower()

    def test_friend_command_runs(self):
        """Friend command runs when given appropriate cmdline options."""
        friendcmd = spcmd.get_command("friends")
        cli = utils.SettableClientProvider()
        cli.set_friends = [
            sptype.FriendInformation(name="d3r3kk", user_id="12345"),
            sptype.FriendInformation(name="other", user_id="67890"),
        ]
        self.cfg.command_args_val = []
        out = friendcmd.run(self.cfg, cli)
        assert out
        assert len(out) == 2
        for row in out:
            assert "d3r3kk" in row or "other" in row

    def test_friend_force(self):
        """Friend command issues the '-f' flag correctly and runs when it is issued."""
        friendcmd = spcmd.get_command("friends")
        cli = utils.SettableClientProvider()
        cli.set_friends = [
            sptype.FriendInformation(name="d3r3kk", user_id="12345"),
            sptype.FriendInformation(name="other", user_id="67890"),
        ]
        self.cfg.force_flag = True
        out = friendcmd.run(self.cfg, cli)
        assert cli.get_friends_forced is True
        for row in out:
            assert "d3r3kk" in row or "other" in row
