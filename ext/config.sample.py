# This file should generally become
# less useful as you scroll down.

# Discord api key
token = ""
# Bot prefix
prefix = "."
# Api key from sendgrid
sg_apikey = ""
# How do you call your server
servername = "727"
# Bot ID
bot_id = ""
# Bot owner(s), people with full access to (almost) everything, skips permission checks
bot_owners = ["123456789012345678"]

# Sql login cridentials
sql = {
        "host": "server ip",
        "user": "user",
        "password": "password",
        "db": "database",
}

#* Your server domains
domains = {
    # Main domain
    "main": "your.domain",
    # Api domain, by default osu.your.domain
    "api": "osu.your.domain",
    # Avatar server domain, by default #osu.your.domain
    "avatar": "a.your.domain",
}

#* Control which modules should be turned on or off
modules = {
    #! Remember to capitalize True or False, otherwise it will break. (Python moment)

    # Mailing service (.sendmail, etc)
    # Requiers sendgrid api key, you can get it at sendgrid.com
    "mailer": True,

    # Osu related stuff, profiles, scores etc.
    "osu": True,

    # Admin module, managing server and users. I strongly recommend reaing permissions of these commands
    "admin": True
}

#* Control which commands should be turned on or off
commands = {
             # Remember that if you turned off module, commands will be turned off too
    #! Remember to capitalize True or False, otherwise it will break. (Python moment)

    # Osu module
    "best": True,
    "rs": True,
    "profile": True,
    "leaderboard": True,
    
    # Mailer
    "sendmail": True,
    "sendtemplate": True,

    # Administration
    "checknotes": True,
    
}