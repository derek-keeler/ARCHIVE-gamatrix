import dataclasses

"""Useful types specific to the Gamatrix application."""


class GamatrixExit(Exception):
    """Tell the interactive loop that it's time to exit the app."""

    pass


@dataclasses.dataclass
class FriendInformation:
    name: str
    user_id: str


# Possible data we can store for a game:
#
# 'appid':10
# 'has_community_visible_stats':True
# 'img_icon_url':'6b0312cda02f5f777efa2f3318c307ff9acafbb5'
# 'img_logo_url':'af890f848dd606ac2fd4415de3c3f5e7a66fcb9f'
# 'name':'Counter-Strike'
# 'playtime_forever':9
# 'playtime_linux_forever':0
# 'playtime_mac_forever':0
# 'playtime_windows_forever':0


@dataclasses.dataclass
class GameInformation:
    name: str
    appid: str
