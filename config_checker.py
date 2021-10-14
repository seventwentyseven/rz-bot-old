from os import truncate
import config
from const.colors import colors
chccfg = "check your config and compare it with config.sample.py"
r = colors.red
e = colors.end
y = colors.yellow
def checkConfig():
    print(f"{y}Checking config{e}")
    #Check if bot token value exists
    try:
        x = config.token
    except:
        print(f"{r}ERROR: Bot token variable does not exist, {chccfg}{e}")
        exit()

    if config.token == "your bot token" or len(config.token) == 0:
        print(f"{r}ERROR: You must set your bot token{e}")
        exit()

    #Bot id
    try:
        x = config.bot_id
    except:
        print(f"{r}ERROR: Bot id variable does not exist, {chccfg}{e}")
        exit()
    if config.bot_id == "your bot id" or len(config.bot_id) == 0:
        print(f"{r}ERROR: You must set your bot id{e}")
        exit()

    #Sql
    try:
        x = config.sql
    except:
        print(f"{r}ERROR: SQL dict does not exist, {chccfg}{e}")
        exit()

    #Bot owners
    try:
        x = config.bot_owners
    except:
        print(f"{r}ERROR: Bot owners list does not exist, {chccfg}{e}")
        exit()
    if len(config.bot_owners) == 0:
        print(f"{r}ERROR: You must set up at least one owner in owners list{e}")
        exit()
    if config.bot_owners[0] == "discord id 1":
        print(f"{r}ERROR: You must set up at least one owner in owners list{e}")
        exit()

    #prefix
    try:
        x = config.prefix
    except:
        print(f"{r}ERROR: Prefix variable does not exist, {chccfg}{e}")
        exit()
    if config.prefix == "":
        print(f"{r}ERROR: Prefix variable is empty{e}")
        exit()

    #servername
    try:
        x = config.servername
    except:
        print(f"{r}ERROR: Servername variable does not exist, {chccfg}{e}")
        exit()
    if config.servername == "your server name":
        print(f"{r}ERROR: You must set up your own servername{e}")
        exit()

    #Bot name
    try:
        x = config.bancho_bot_name
    except:
        print(f"{r}ERROR: Banchobot variable does not exist, {chccfg}{e}")
        exit()

    #Sg apikey
    try:
        x = config.sg_apikey
    except:
        print(f"{r}ERROR: Sg apikey variable does not exist, {chccfg}{e}")
        exit()

    #updater enabled?
    try:
        x = config.updater_enabled
    except:
        print(f"{r}ERROR: Updater variable does not exist, {chccfg}{e}")
        exit()
    try:
        x = bool(config.updater_enabled)
    except:
        print(f"{r}ERROR: Updater variable must be exactly True or False{e}")
        exit()

    #Update checktime
    try:
        x = config.update_check_time
    except:
        print(f"{r}ERROR: Updater check time variable does not exist, {chccfg}{e}")
        exit()
    try:
        x = int(config.update_check_time)
    except:
        print(f"{r}ERROR: Updater check time variable must be WHOLE number (integer){e}")
        exit()

    #domains
    try:
        x = config.domains
    except:
        print(f"{r}ERROR: Domains dict does not exist, {chccfg}{e}")
        exit()
    try:
        x = config.domains['main']
    except:
        print(f"{r}ERROR: main value in domains dict does not exist, {chccfg}{e}")
        exit()
    try:
        x = config.domains['api']
    except:
        print(f"{r}ERROR: api value in domains dict does not exist, {chccfg}{e}")
        exit()
    try:
        x = config.domains['avatar']
    except:
        print(f"{r}ERROR: Avatar value in domains dict does not exist, {chccfg}{e}")
        exit()

    #emails
    try:
        x = config.emails
    except:
        print(f"{r}ERROR: Emails dict does not exist, {chccfg}{e}")
        exit()

    #channels
    try:
        x = config.channels
    except:
        print(f"{r}ERROR: Channels dict does not exist, {chccfg}{e}")
        exit()
    keys = []
    true_keys = ["gulaglogs", "botlogs", "modlogs", "rankeds", "verificationlogs",
                 "admin_stuff", "admin_chat", "staff_general", "mod_chat", "owner_chat"]
    for key, value in config.channels.items() :
        keys.append(key)
        if value == "id":
            print(f"{y} Channels dict: {key} value unset, check it and set it yourself")
    for i in true_keys:
        if i not in keys:
            print(f"{r}ERROR: {i} Value Is not present in channels dict, {chccfg}{e}")
            exit()

    #roles
    try:
        x = config.roles
    except:
        print(f"{r}ERROR: Roles dict does not exist, {chccfg}{e}")
        exit()
    keys = []
    true_keys = ["dangerous", "dev", "admin", "mod", "bat", "alumni", "donatorp", "donator",
                 "restricted", "verified", "normal", "nicknameban"]
    for key, value in config.roles.items() :
        keys.append(key)
        if value == "id":
            print(f"{y} Roles dict: {key} value unset, check it and set it yourself")
    for i in true_keys:
        if i not in keys:
            print(f"{r}ERROR: {i} Value Is not present in roles dict, {chccfg}{e}")
            exit()

    #emotes
    try:
        x = config.emotes
    except:
            print(f"{r}ERROR: {i} Emotes dict does not exist, {chccfg}{e}")
            exit()

    #modules
    try:
        x = config.modules
    except:
        print(f"{r}ERROR: {i} Modules dict does not exist, {chccfg}{e}")
        exit()
    true_keys = ["mailer", "osu", "admin"]
    for key, value in config.modules.items() :
        if key not in true_keys:
            print(f"{r}ERROR: {key} Value in modules dict does not exist, {chccfg}{e}")
            exit()
        else:
            if value not in [True, False]:
                print(f"{r}ERROR: {key} Value in modules dict must be exactly True or False, {chccfg}{e}")
                exit()

    #commands
    try:
        x = config.commands
    except:
        print(f"{r}ERROR: {i} Commands dict does not exist, {chccfg}{e}")
        exit()
    true_keys = ["best", "rs", "profile", "leaderboard", "sendmail",
                 "sendtemplate", "checknotes", "changecountry", "givedonator"]
    for key, value in config.commands.items() :
        if key not in true_keys:
            print(f"{r}ERROR: {key} Value in commands dict does not exist, {chccfg}{e}")
            exit()
        else:
            if value not in [True, False]:
                print(f"{r}ERROR: {key} Value in commands dict must be exactly True or False, {chccfg}{e}")
                exit()

    # Restrict admin commands
    try:
        x = config.restrict_admin_commands
    except:
        print(f"{r}ERROR: Restrict admin commands value does not exist, {chccfg}{e}")
        exit()
    try:
        x = bool(config.restrict_admin_commands)
    except:
        print(f"{r}ERROR: Restrict admin commands value must be exactly True or False, {chccfg}{e}")
        exit()

    #Restricted access
    try:
        x = config.restricted_access
    except:
        print(f"{r}ERROR: {i} restricted access dict does not exist, {chccfg}{e}")
        exit()
    true_keys = ["best", "rs", "profile"]
    for key, value in config.restricted_access.items() :
        if key not in true_keys:
            print(f"{r}ERROR: {key} Value in restricted access dict does not exist, {chccfg}{e}")
            exit()
        else:
            if value not in [True, False]:
                print(f"{r}ERROR: {key} Value in restricted access dict must be exactly True or False, {chccfg}{e}")
                exit()
    # Restrict admin commands
    try:
        x = config.restricted_users_view_by_all
    except:
        print(f"{r}ERROR: Restricted users view by all value does not exist, {chccfg}{e}")
        exit()
    try:
        x = bool(config.restricted_users_view_by_all)
    except:
        print(f"{r}ERROR: Restricted users view by all value must be exactly True or False, {chccfg}{e}")
        exit()

    #Footer type
    try:
        x = config.footer_type
    except:
        print(f"{r}ERROR: Footer type value does not exist, {chccfg}{e}")
        exit()
    try:
        x = int(config.footer_type)
    except:
        print(f"{r}ERROR: Footer type value must be WHOLE number (integer){e}")

    #Options best
    try:
        x = config.opt_best
    except:
        print(f"{r}ERROR: Opt best dict does not exist, {chccfg}{e}")
        exit()
    try:
        x = config.opt_best['min_g_value']
        x = config.opt_best['g_fetch_failed']
    except:
        print(f"{r}ERROR: Some value in opt best does not exist, {chccfg}{e}")
        exit()
    if config.opt_best['g_fetch_failed'] not in [True, False]:
        print(f"{r}ERROR: g_fetch_failed value in opt_best must be exactly True or False{e}")
        exit()
    try:
        x = int(config.opt_best['g_fetch_failed'])
    except:
        print(f"{r}ERROR: min_g_value value in opt_best must be WHOLE number (integer){e}")
        exit()

    #No catch
    try:
        x = config.no_catch
    except:
        print(f"{r}ERROR: No catch value in opt best does not exist, {chccfg}{e}")
        exit()
    if config.no_catch not in [True, False]:
        print(f"{r}ERROR: No catch must be exactly True or False{e}")
        exit()

    #Contact
    try:
        x = config.contact
    except:
        print(f"{r}ERROR: Contact dict in opt best does not exist, {chccfg}{e}")
        exit()
    try:
        x = config.contact['email']
    except:
        print(f"{r}ERROR: Email value in contact dict in opt best does not exist, {chccfg}{e}")
        exit()
    try:
        x = config.contact['discord']
    except:
        print(f"{r}ERROR: Discord value in contact dict in opt best does not exist, {chccfg}{e}")
        exit()

    #Templates
    try:
        x = config.mailtemplates
    except:
        print(f"{r}ERROR: Mailtemplates dict does not exist, {chccfg}{e}")
        exit()

    template_structure = ["title", "email_content", "email_used"]
    for key, value in x.items():
        for template_key in value.keys():
            if template_key not in template_structure:
                print(f"{r}ERROR in Mailtemplates: Template Name: {key} Template must have email, email content and email used {chccfg}{e}")
                exit()
        if value['email_used'] not in config.emails.values():
            print(f"{r}ERROR: Mailtemplates: Template name: {value} Specified email not found in email value")
            exit()

    return print(f"{colors.green}Config checked, no problems found\n{e}")