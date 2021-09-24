# -*- coding: utf-8 -*-

from enum import IntFlag
from enum import unique



@unique
class Privileges(IntFlag):
    """Server side user privileges."""

    # privileges intended for all normal players.
    Normal      = 1 << 0 # is an unbanned player.
    Verified    = 1 << 1 # has logged in to the server in-game.

    # has bypass to low-ceiling anticheat measures (trusted).
    Whitelisted = 1 << 2

    # donation tiers, receives some extra benefits.
    Supporter   = 1 << 4
    Premium     = 1 << 5

    # notable users, receives some extra benefits.
    Alumni      = 1 << 7

    # staff permissions, able to manage server state.
    Tournament  = 1 << 10 # able to manage match state without host.
    Nominator   = 1 << 11 # able to manage maps ranked status.
    Mod         = 1 << 12 # able to manage users (level 1).
    Admin       = 1 << 13 # able to manage users (level 2).
    Dangerous   = 1 << 14 # able to manage full server state.

    Donator = Supporter | Premium
    Staff = Mod | Admin | Dangerous

prv_list = {
    "normal": 1,
    "verified": 2,
    "whitelisted": 4,
    "supporter": 16,
    "premium": 32,
    "alumni": 128,
    "tournament": 1024,
    "nominator": 2048,
    "mod": 4096,
    "admin": 8192,
    "dangerous": 16384
}

prv_list_rev = {
    1: "normal",
    2: "verified",
    4: "whitelisted",
    16: "supporter",
    32: "premium",
    128: "alumni",
    1024: "tournament",
    2048: "nominator",
    4096: "mod",
    8192: "admin",
    16384: "dangerous"
}
