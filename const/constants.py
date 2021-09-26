import cmyui

#Don't touch it. I'm changing it on updates, it's also (will be) used for updater
version = cmyui.Version(0, 3, 5)

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
    0: 'Idle: 🔍 Selecting a song',
    1: 'Idle: 🌙 AFK',
    2: 'Playing: 🎶 ',
    3: 'Editing: 🔨 ',
    4: 'Modding: 🔨 ',
    5: 'In Multiplayer: Selecting 🏯 ',
    6: 'Watching: 👓 ',
    8: 'Testing: 🎾 ',
    9: 'Submitting: 🧼 ',
    10: 'Paused: 🚫 ',
    11: 'Idle: 🏢 In multiplayer lobby',
    12: 'In Multiplayer: Playing 🌍 ',
    13: 'Idle: 🫒 Downloading some beatmaps in osu!direct',
    'default': 'Unknown: 🚔 not yet implemented!',
}