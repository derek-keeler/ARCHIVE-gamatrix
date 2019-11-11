"""Test out the friends command."""

import docopt  # type: ignore

import steamingpile.commands as spcmd
import steamingpile.types as sptype
from . import stubs


class TestFriendsCommand:

    # standard config not used for doing anything in this case.
    cfg = stubs.Config()

    def test_friend_command_exists(self):
        """Friend command exists and is the right type."""
        friendcmd, args = spcmd.get_command("friends", self.cfg)
        assert friendcmd
        assert isinstance(friendcmd, spcmd.Friends)

    def test_friend_command_fails(self):
        """Friend command fails when spelled incorrectly."""
        friendcmd, args = spcmd.get_command("fren", self.cfg)
        cli = stubs.SettableClientProvider()
        out = friendcmd.run(args, cli)
        assert "unknown" in out[0].lower()

    def test_friend_fails_bad_cmdline(self):
        """Friend command fails when given unknown commandline argument, and gives appropriate feedback."""
        friendcmd, args = spcmd.get_command("friends --do-something-not-allowed", self.cfg)
        cli = stubs.SettableClientProvider()
        cli.set_friends = [
            sptype.FriendInformation(name="d3r3kk", user_id="12345"),
            sptype.FriendInformation(name="other", user_id="67890"),
        ]
        try:
            friendcmd.run(args, cli)
        except docopt.DocoptExit as e:
            assert "friends" in e.usage.lower()
            assert "--force" in e.usage.lower()
        else:
            assert "Argument parsing for friends command did not recognize bad input." == ""

    def test_friend_command_runs(self):
        """Friend command runs when given appropriate cmdline options."""
        friendcmd, args = spcmd.get_command("friends", self.cfg)
        cli = stubs.SettableClientProvider()
        cli.set_friends = [
            sptype.FriendInformation(name="d3r3kk", user_id="12345"),
            sptype.FriendInformation(name="other", user_id="67890"),
        ]
        out = friendcmd.run(args, cli)
        assert out
        assert len(out) == 2
        for row in out:
            assert "d3r3kk" in row or "other" in row

    def test_friend_force_shortflag(self):
        """Friend command issues the '-f' flag correctly and runs when it is issued."""
        friendcmd, args = spcmd.get_command("friends -f", self.cfg)
        cli = stubs.SettableClientProvider()
        cli.set_friends = [
            sptype.FriendInformation(name="d3r3kk", user_id="12345"),
            sptype.FriendInformation(name="other", user_id="67890"),
        ]
        out = friendcmd.run(args, cli)
        assert cli.get_friends_forced is True
        for row in out:
            assert "d3r3kk" in row or "other" in row

    def test_friend_force_longflag(self):
        """Friend command issues the '--force' flag correctly and runs when it is issued."""
        friendcmd, args = spcmd.get_command("friends --force", self.cfg)
        cli = stubs.SettableClientProvider()
        cli.set_friends = [
            sptype.FriendInformation(name="d3r3kk", user_id="12345"),
            sptype.FriendInformation(name="other", user_id="67890"),
        ]
        out = friendcmd.run(args, cli)
        assert cli.get_friends_forced is True
        for row in out:
            assert "d3r3kk" in row or "other" in row
