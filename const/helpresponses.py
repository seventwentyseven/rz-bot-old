from const import glob
from const.privileges import Privileges
p = glob.config.prefix
helpresponses = {
    "profile": {
        "privileges": Privileges.Normal,
        "header": "Profile",
        "description": "Shows info about user",
        "example": f"`{p}profile -u def750 -m taiko -rx`",
        "info": "Arguments: \n`-m` - Specify mode. You can use mode name like `mania` or mode number like `1`\n`-u` - Specify user, you can mention them or type their name on server"+ 'Remember that if user has dashes in their name you need to specify it in `"` like `"- def750 -"`' +"\n`-rx` and `-ap` - Specify if you want to see profile in relax or autopilot"
    },
    "best": {
        "privileges": Privileges.Normal,
        "header": "Best",
        "description": "Shows user's best scores",
        "example": f"`{p}best -u def750 -m 0 -ap -n 1` or `{p}best -u def750 -m 0 -rx -g 300`",
        "info": "Arguments: \n`-m` - Specify mode. You can use mode name like `mania` or mode number like `1`\n`-u` - Specify user, you can mention them or type their name on server"+ 'Remember that if user has dashes in their name you need to specify it in `"` like `"- def750 -"`' +"\n`-rx` and `-ap` - Specify if you want to see profile in relax or autopilot\n`-g` - Shows amount of scores that user has over `x` pp\n`-n` - Best score number"
    },
    "rs": {
        "privileges": Privileges.Normal,
        "header": "Recent",
        "description": "Shows user's most recent score",
        "example": f"`{p}usage`",
        "info": "Arguments: \n`-m` - Specify mode. You can use mode name like `mania` or mode number like `1`\n`-u` - Specify user, you can mention them or type their name on server"+ 'Remember that if user has dashes in their name you need to specify it in `"` like `"- def750 -"`' +"\n`-rx` and `-ap` - Specify if you want to see profile in relax or autopilot"
    },
    "link": {
        "privileges": Privileges.Normal,
        "header": f"Link",
        "description": f"Link your {glob.config.servername} account to discord",
        "example": f"`{p}link 21345`",
        "info": "Arguments:\n `<5-digit code>` - Code from the bot on osu server\n\n**How to get code?**\n"
            "**1.** Login to your osu account on our server\n"
            "**2.** Click `F9` and, and search for `Ż Bot`, it's our bancho bot\n"
            "**3.** Open chat with `Ż Bot` and type `!link <your discord tag>`, for example `!link def750#2137`\n"
            f"**4.** Bot will give you 5-digit code, return to discord and type `{p}link <code that you recieved>`\n"
            "After this you should be done, if you still have problem feel free to ask staff for help",
    },
    "rlc": {
        "privileges": Privileges.Dangerous,
        "header": "rlc",
        "description": "Reloads cog",
        "example": f"`{p}rlc admin`",
        "info": "Arguments: \n`<cog name>` - Specify cog (module)"
    },
    "load": {
        "privileges": Privileges.Dangerous,
        "header": "Load",
        "description": "Loads cog",
        "example": f"`{p}load admin`",
        "info": "Arguments: \n`<cog name>` - Specify cog (module)"
    },
    "getuserid": {
        "privileges": Privileges.Normal,
        "header": "Get user id",
        "description": "Get id of specified user",
        "example": f"`{p}getuserid <def750>`",
        "info": f"Arguments: \n`<user>` - Specify user ({glob.config.servername} name)"
    },

}