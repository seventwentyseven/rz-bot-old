import cmyui
import aiohttp
session = aiohttp.ClientSession()
#Don't touch version or else updater will get autism. I'm the one changing it, not you.
version = cmyui.Version(1, 0, 1)

#Don't touch this too, it's mysql connection stuff
db = cmyui.AsyncSQLPool()
rx_modes = {
    "0": "4",
    "1": "5",
    "2": "6"
}

mode_names = {
    "0": "Standard",
    "1": "Taiko",
    "2": "Catch",
    "3": "Mania"
}

mods_full_names = {
    "vn": "vanilla",
    "rx": "relax",
    "ap": "autopilot",
}

modes = {
    "osu": "0",
    "taiko": "1",
    "catch": "2",
    "mania": "3",
    "std": "0",
    "o": "0",
    "t": "1",
    "c": "2",
    "m": "3",
    "0": "0",
    "1": "1",
    "2": "2",
    "3": "3"
}

#Copied and translated to python from guweb
actions_statuses = {
    0: 'Idle: ๐ Selecting a song',
    1: 'Idle: ๐ AFK',
    2: 'Playing: ๐ถ ',
    3: 'Editing: ๐จ ',
    4: 'Modding: ๐จ ',
    5: 'In Multiplayer: Selecting ๐ฏ ',
    6: 'Watching: ๐ ',
    8: 'Testing: ๐พ ',
    9: 'Submitting: ๐งผ ',
    10: 'Paused: ๐ซ ',
    11: 'Idle: ๐ข In multiplayer lobby',
    12: 'In Multiplayer: Playing ๐ ',
    13: 'Idle: ๐ซ Downloading some beatmaps in osu!direct',
    'default': 'Unknown: ๐ not yet implemented!',
}
