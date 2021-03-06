# This file should generally become
# less useful as you scroll down.

##############################
#        MAIN SECTION        #
##############################
# Discord api key
token = "your bot token"
# Bot ID
bot_id = "your bot id"
# Sql login cridentials
sql = {
    "host": "sql db ip",
    "user": "sql user",
    "password": "sql password",
    "db": "gulag",
}
# Bot owner(s), people with full access to (almost) everything, skips permission checks
bot_owners = [
    "discord id 1", #you can put owner username to know who you addced here
    "discord id 2", #dzifors, you can look at how it looks and add another owner or delete one
                    #you can also always ask me for help
]
# Bot prefix
prefix = "."
# How do you call your server
servername = "your server name"
# Your bancho bot name (on osu server)
bancho_bot_name = "Ż Bot"
# Api key from sendgrid
sg_apikey = "sendgrid api key"

# Should be update checker turned on?
updater_enabled = True
# How often should bot check for updates (in minutes)
update_check_time = 10

#######################
#      CONSTANTS      #
#######################
#* Your server domains, REMEMBER THAT YOU NEED HTTPS CERT, you can easly issue it with certbot
domains = {
    # Main domain
    "main": "your.domain",
    # Api domain, by default osu.your.domain
    "api": "osu.your.domain",
    # Avatar server domain, by default #a.your.domain
    "avatar": "a.your.domain",
}

#Your email list, no need to change it if you are not going to use mailer module
# If you're gonna use it, i recommend going into mailtemplates and setting up your emails
emails = {
    "admin": "admin@your.domain",
    "support": "support@your.domain",
    "accounts": "accounts@your.domain",
}

# Channel config
channels = {
    #If you use one chat for multiple logs, just set same ID, it doesn't matter
    #Logs from gulag
    "gulaglogs": "id",
    #Bot action logs
    "botlogs": "id",
    #Moderation logs
    "modlogs": "id",
    #New rankeds loveds and unrankeds
    "rankeds": "id",
    #Logs of verification
    "verificationlogs": "id",

    # Admin category id
    "admin_stuff": "id",
    #Administration chats, If you dont have some of these just set one id for one or few of them
    "admin_chat": "id",
    "staff_general": "id",
    "mod_chat": "id",
    "owner_chat": "id"
}
# Role Config
roles = {
    #Developer/owner
    "dangerous": "id",
    #Developer
    "dev": "id",
    "admin": "id",
    #Aka. GMT
    "mod": "id",
    #Beatmap nominator
    "bat": "id",
    #Staff member that is no longer staff
    "alumni": "id",
    #Premium
    "donatorp": "id",
    #Donator
    "donator": "id",
    "restricted": "id",
    #User that connected osu account to discord
    "verified": "id",
    #Normal user
    "normal": "id",
    #Prevents from changing nickname
    "nicknameban": "id"
}

#Used in embeds, it's explained in readme.
# If you are too lazy to add it yourself, ask me on dms (def750#2137) I'll add your bot to our emote server
emotes = {
    "F": "<:rankf:853753898954391572>",
    "D": "<:rankd:853753898682155009>",
    "C": "<:rankc:853753898912448553>",
    "B": "<:rankb:853753899089657866>",
    "A": "<:ranka:853753899000004618>",
    "S": "<:ranks:853753899135402044>",
    "SH": "<:ranksh:853753899072094208>",
    "X": "<:rankx:853753898817028147>",
    "XH": "<:rankxh:853753899206311976>",
}

##############################
#    TURN THINGS OFF / ON    #
##############################
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
    "changecountry": True,
    "givedonator": True

}

#############################
#    COMMAND RESTRICTION    #
#############################
#Should usage of admin commands be restricted only to admin channels
#I strongly recommend leaving that as true due to users privacy.
restrict_admin_commands = True

#Should restricted people have access to specific commands
restricted_access = {
    "best": False,
    "profile": False,
    "rs": False,
}

#Can users view profiles of restricted users or only admins can do that?
restricted_users_view_by_all = False

##########################
#      EMBED CONFIG      #
##########################

#*Select footer type:
# 0: Bot Version: {version} | Bot Creator: def750#2137
# 1: Bot Version: {version} | On {server_name}
# 2: On {server_name} | Bot Version: {server_name}
# 3: On {server_name} Bot Version: {version} | Bot Creator: def750#2137
# 4: Bot Version: {version}
# 5: Version: {version}
# 6: On: {server_name}
# If you want to edit it or add new, they are in main.py
footer_type = 0

# Exec command, aviable only for bot owners specified above. It allows to directly
# execute python script so it's extremelly dangerous.
exec_cmd = True

#NOTE: To change colors of embeds go to the const/colors.py file

###################################
#     COMMAND SPECIFIC OPTIONS    #
###################################

# Best command
opt_best = {
    # Minimum pp for -g argument in best command,
    # keep it above 15 to avoid lags with database
    "min_g_value": 20,
    # Should -g argument fetch failed scores
    # Default: False
    "g_fetch_failed": False
}
#Funi texts for people who hate catch like us
no_catch = True

#Contact stuff for emails
contact = {
    "email": "seven27tk@gmail.com",
    "discord": "def750#2137"
}

#Customise it if you're gonna use mailer module
mailtemplates = {
    "cheating": {
        "title": f"{servername} - Account restricted", #Email title
        "email_content": "Your account has been restricted for cheating<br>" #Email content
                        f"If you think that account restriction has been unfairly imposed contact us on"
                        f" {contact['email']} or send DM to {contact['discord']} on discord"
                        f"<br><br>Regards, {servername} support.", #<br> is line break (new line)
        "email_used": emails['accounts'] #Email that will be used to send email, specified above
    },
    "pp_limit": {
        "title": f"{servername} - Account restricted",
        "email_content": "Your account has been restricted for reaching pp limit (700)<br>" #Set your own pp value of autoban corresponding to gulag config
                        f"If you think that account restriction has been unfairly imposed contact us on "
                        f" {contact['email']} or send DM to {contact['discord']} on discord"
                        f"<br><br>Regards, {servername} support.",
        "email_used": emails['accounts']
    },
    "multiaccounting": {
        "title": f"{servername} - Account restricted",
        "email_content": "Your account has been restricted for multiaccounting"
                        f"If you think that account restriction has been unfairly imposed contact us on "
                        f" {contact['email']} or send DM to {contact['discord']} on discord"
                        f"<br><br>Regards, {servername} support.",
        "email_used": emails['accounts']
    },
    "impersonation": {
        "title": f"{servername} - Account restricted",
        "email_content": "Your account has been restricted for impersonation"
                        f"If you think that account restriction has been unfairly imposed contact us on "
                        f" {contact['email']} or send DM to {contact['discord']} on discord"
                        f"<br><br>Regards, {servername} support.",
        "email_used": emails['accounts']
    },
}