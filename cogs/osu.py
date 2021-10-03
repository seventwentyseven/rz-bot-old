import discord
from discord.ext import commands
from discord.user import Profile

from cmyui import log, Ansi, utils
from cmyui.osu import Mods
import datetime
import json
import pandas
import requests
from requests import api

from const.colors import colors
from const import constants as const
from const import glob
from const import mods
from const.privileges import Privileges

from utils import time as tu
from utils.utils import parseArgs, getUserGroupList


#Re define for easier usage
prefix = glob.config.prefix
version = const.version
roles = glob.config.roles
emotes = glob.config.emotes

class osu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
            

def setup(bot):
    bot.add_cog(osu(bot))
    bot.add_command(profile)
    bot.add_command(best)
    bot.add_command(rs)

@commands.command()
async def profile(ctx, *args):
    """Check user profile and their stats"""
    allowed_args = ["-u", "-rx", "-ap", "-m"]
    cmd_name = "profile"
    args_as_list = args

    #!Check if module & command disabled
    if glob.config.modules["osu"] == False:
        embed = discord.Embed(
            title="Error", 
            description="This module has been disabled by administrator.", 
            color=colors.embeds.red)
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    if glob.config.commands["profile"] == False:
        embed = discord.Embed(
            title="Error", 
            description="This command has been disabled by administrator.", 
            color=colors.embeds.red)
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
        
    #!Check if user is restricted (role)
    if glob.config.restricted_access['profile'] == False:
        #TODO: Optimize this, as for loop for just roles is stupid idea but works for now
        for role in ctx.author.roles:           #getting all roles of member
            if role.id == int(roles['restricted']):
                #! THIS CHECKS FOR ROLE, NOT PERMS
                # Perm check from osu is in config and lower part of code.
                # Under restricted_users_view_by_all and restricted_access
                embed = discord.Embed(title="Error", 
                description=f"You can't use `{prefix}{cmd_name}` because you're restricted!", 
                color=colors.embeds.red
                )
                embed.set_footer(text=glob.embed_footer)
                return await ctx.send(embed=embed)

    #!Parse arguments
    args = parseArgs(args, allowed_args)

    #*Check if first thing argument is not allowed
    if len(args_as_list) == 0:
        pass
    elif args_as_list[0] not in allowed_args:
        embed = discord.Embed(title="Error", 
        description=f"First argument is incorrect, check `{prefix}help {cmd_name}` if you need help", 
        color=colors.embeds.red
        )
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    
    #! Parse user
    if "-u" in args:
        if len(args["-u"]) > 15:
            # Max nick length on server is 15, so if it's over 15
            # it will be mention, otherwise it won't find user after all ;)

            # Cut <! and > from mention to leave id
            user = args["-u"][3:-1]
            if str(ctx.author.id) == str(user):
                self_execute = True
                desc1 = f"You don't have your osu profile linked, type `{prefix}help link` if you need help.\n You can always try with your 727 name\nRemember that names like `-u s e r-` must be put in quotation marks for example "+'`.profile -u "-u s e r-"`\n'
            else:
                self_execute = False
                desc1 = f"User not found, maybe they don't have discord connected?\n You can also try with their 727.tk username\nRemember that names like `-u s e r-` must be put in quotation marks for example "+'`.profile -u "-u s e r-"`\n'
            
            #* Database stuff
            user_discord = await glob.db.fetch(
                "SELECT osu_id, default_mode, discord_id FROM discord WHERE discord_id = %s", user
            )
            
            #! User not found, in this case not linked
            if not user_discord:
                embed = discord.Embed(title="Error",
                description=f"{desc1}.\nIf you need help with this command type `{prefix}help {cmd_name}`", 
                color=colors.embeds.red)
                embed.set_footer(text=glob.embed_footer)
                return await ctx.send(embed=embed)
            
            #* Get osu info
            userid = user_discord["osu_id"]
            user_osu = await glob.db.fetch(
                "SELECT id, name, priv, country,"
                "silence_end, creation_time,"
                "latest_activity, clan_id, clan_priv "
                "FROM users WHERE id = %s", userid
            )
        else:
            # It was bancho name all along
            user = args["-u"]
            if user.startswith('"') and user.endswith('"'):
                user = user[1:-1]
            user_osu = await glob.db.fetch(
                "SELECT id, name, priv, country,"
                "silence_end, creation_time,"
                "latest_activity, clan_id, clan_priv "
                "FROM users WHERE name = %s", user
            )
            if not user_osu:
                embed = discord.Embed(title="Error",
                description=f"User not found, maybe they don't have discord connected?\n"
                             "You can also try with their 727.tk username\nRemember that " 
                             "names like `-u s e r-` must be put in quotation marks for example "
                             '`.profile -u "-u s e r-"`\n'
                             f"\nIf you need help with this command type `{prefix}help {cmd_name}`",
                color=colors.embeds.red)
                embed.set_footer(text=glob.embed_footer)
                return await ctx.send(embed=embed)
            user_oid = user_osu['id']
            user_discord = await glob.db.fetch(
                "SELECT discord_id, default_mode FROM discord WHERE osu_id = %s", user_oid
            )
            if user_discord and str(user_discord['discord_id']) == str(ctx.author.id):
                self_execute = True
            else:
                self_execute = False
    else:
        #Not specified, get author id and check if linked
        user = ctx.author.id
        self_execute = True
        
        #* Database stuff
        user_discord = await glob.db.fetch(
            "SELECT osu_id, default_mode, discord_id FROM discord WHERE discord_id = %s", user
        )
        #! User not found, in this case not linked
        if not user_discord:
            embed = discord.Embed(
                title="Error",
                description=f"You don't have your osu profile linked, type `{prefix}help link` "
                            f"if you need help.\nYou can always try with your 727 name"
                            f"\nRemember that names like `-u s e r-` must be put in quotation marks "
                            f"for example "+'`.profile -u "-u s e r-"`'
                            f"\nIf you need help with this command type `{prefix}help {cmd_name}`", 
                color=colors.embeds.red)
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed)
        
        #* Get osu info
        userid = user_discord["osu_id"]
        user_osu = await glob.db.fetch(
            "SELECT id, name, priv, country,"
            "silence_end, creation_time,"
            "latest_activity, clan_id, clan_priv "
            "FROM users WHERE id = %s", userid
        )

    userid = user_osu['id']
    #!Ż bot is uncheckable
    if user_osu['id'] == 1:
        embed = discord.Embed(
        title="Error", 
        description=f"Well, you can't check {glob.config.bancho_bot_name} on discord. For some reason it just won't work",
        color=colors.embeds.red)
        embed.set_footer(text=f"Bot Version: {version}")
        return await ctx.send(embed=embed)

    #Also make sure to get author perms !Not checked if turned off in config
    if glob.config.restricted_users_view_by_all == False:
        author_discord = await glob.db.fetch(
            "SELECT osu_id FROM discord WHERE discord_id = %s", ctx.author.id
        )
        if author_discord:
            author_oid = author_discord['osu_id']
            author_osu = await glob.db.fetch("SELECT priv FROM users WHERE id = %s", author_oid)
        else:
            author_osu = {
                "priv": 3
            }
        user_priv = Privileges(int(user_osu['priv']))
        author_priv = Privileges(int(author_osu['priv']))
        #! Check if restricted, if yes check if allowed in config, in no check perms, 
        #! if yes check admin commands allowed in public, if no check channel
        if not user_priv & Privileges.Normal and not glob.config.restricted_users_view_by_all:
        # user is restricted and only admins can do this, we should check if they are allowed to use it in this channel or not
            if not author_priv & Privileges.Staff:
                embed = discord.Embed(
                    title="Error", 
                    description=f"You don't have permissions to check profiles of restricted users.", 
                    color=colors.embeds.red)
                embed.set_footer(text=glob.embed_footer)
                return await ctx.send(embed=embed)

            if glob.config.restrict_admin_commands == True and str(ctx.channel.category_id) != glob.config.channels['admin_stuff']:
                embed = discord.Embed(
                    title="Error", 
                    description=f"Due to security reasons, viewing restricted people profiles is only available in admin channels", 
                    color=colors.embeds.red)
                embed.set_footer(text=glob.embed_footer)
                return await ctx.send(embed=embed)

    # continue as normal here if they aren't restricted/they are allowed to view profile
    #! FINALLY CHECK MODE
    if "-m" in args:
        try:
            mode = str(const.modes[args["-m"].lower()])
        except:
            embed = discord.Embed(title="Invalid Syntax", description=f"Mode is incorrect\nYou can use mode names like `mania` or `std` or mode numbers (`0-3`)\nType `{prefix}help {cmd_name}` if you need help", color=colors.embeds.red)
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed)
    else:
        #! M not specified, get it from user discord, if not existing set std
        if user_discord:
            mode = user_discord['default_mode']
        else:
            mode = "0"

#! Check rx ap and set mode corresponding to it
    # Check rx syntax
    if "-rx" in args and "-ap" in args:
        embed = discord.Embed(title="Invalid Syntax", description=f"Using both `-rx` and `-ap` is not possible\nType `{prefix}help {cmd_name}` if you need help", color=colors.embeds.red)
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    if "-rx" in args:
        if mode == "3":
            embed = discord.Embed(title="Invalid Syntax", description=f"Using `-rx` with mania is not possible\nType `{prefix}help {cmd_name}` if you need help", color=colors.embeds.red)
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed)
        else:
            # Assign mode and mods
            mode_gulag = const.rx_modes[mode]
            mode_mods = "rx"
    # Check ap syntax
    elif "-ap" in args:
        if mode != "0":
            embed = discord.Embed(title="Invalid Syntax", description=f"Using `-ap` in modes other than standard is not possible\nType `{prefix}help {cmd_name}` if you need help", color=colors.embeds.red)
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed)
        else:
            # Assign mode and mods
            mode_gulag = "7"
            mode_mods = "ap"
    else:
    # No mods, assign mode and mods
        mode_gulag = mode
        mode_mods = "vn"
    
    #! API request to get status
    #TODO: Move to aiohttp as this shit below is not async.
    response = requests.get(f"https://{glob.config.domains['api']}/api/get_player_status?id={userid}")
    json_object = json.loads(response.text)
    req = json_object["player_status"]
    
    #* Current Time
    time1 = datetime.datetime.now()
    
    user_api = {}
    if req['online'] == True:
        user_api["status"] = ["🟢", "Online"]
        api_time = datetime.datetime.fromtimestamp(int(req['login_time'])).strftime("%Y-%m-%dT%H:%M:%S")
        api_time = datetime.datetime.strptime(api_time, '%Y-%m-%dT%H:%M:%S')
        user_api["activity"] = tu.time_ago(time1, api_time)
        #*Rest of vars
        api_status = req['status']
        user_api["action"] = api_status['action']
        user_api["info_text"] = api_status['info_text']
        user_api["mode"] = api_status['mode']
        user_api["mods"] = api_status['mods']
        #Text
        user_api["filler1"] = ", logged in"
    else:
        user_api["status"] = ["🔴", "Offline"]
        api_time = datetime.datetime.fromtimestamp(int(req['last_seen'])).strftime("%Y-%m-%dT%H:%M:%S")
        api_time = datetime.datetime.strptime(api_time, '%Y-%m-%dT%H:%M:%S')
        user_api['activity'] = tu.time_ago(time1, api_time)
        user_api['action'] = None
        #Text
        user_api['filler1'] = ", last seen"


    #! Calculate rank
    #! This shit is stupid as fuck, fetching all users with pp>0 is not a good idea
    lb = await glob.db.fetchall("SELECT stats.id FROM stats LEFT JOIN users ON stats.id = users.id WHERE stats.mode = %s && pp>0 && users.priv & 1 ORDER BY pp DESC", mode_gulag)
    try:
        rank_global = int(lb.index({'id': int(userid)}))+1
    except:
        rank_global = 0
    #Country Rank
    usercountry = user_osu['country']
    lb_country = await glob.db.fetchall("SELECT stats.id FROM stats LEFT JOIN users ON stats.id = users.id WHERE stats.mode = %s && users.country = %s && pp>0 && users.priv & 1 ORDER BY pp DESC", (mode_gulag, usercountry))
    try:
        rank_country = int(lb_country.index({'id': int(userid)}))+1
    except:
        rank_country = 0
    

    #!Get user stats
    user_stats = await glob.db.fetch("SELECT * FROM stats WHERE id = %s AND mode = %s", (userid, mode_gulag))
    
    #* Calculate stuff needed for userinfo block
    
    #  Transform user priv to make them look cool 😎
    user_priv = getUserGroupList(user_osu['priv'])
    userpriv = ""
    for el in user_priv:
        userpriv += f" ▸ {el}"

    # Convert timestamps to human readable
    register_date = datetime.datetime.fromtimestamp(int(user_osu['creation_time'])).strftime("%m.%d.%Y %H:%M:%S")
    last_seen_date = datetime.datetime.fromtimestamp(int(user_osu['latest_activity'])).strftime("%m.%d.%Y %H:%M:%S")
    playtime = datetime.timedelta(seconds=user_stats['playtime'])

    # Calculate scores
    rankedscore = "{:,}".format(user_stats['rscore'])
    totalscore = "{:,}".format(user_stats['tscore'])
    #* Build headers for embed
    #* Build embed description
    #*Header (author field)
    embed_header = f"{user_osu['name']}'s Profile"
    
    #*Description header
    embed_dsc_header = f"In osu!{const.mode_names[mode].capitalize()}"
    #Check if mod is vanilla, if not add mod name
    if mode_mods == "vn":
        embed_dsc_header += ""
    else:
        embed_dsc_header += f" with {const.mods_full_names[mode_mods].capitalize()}"

    embed_description = f"▸ **Global Rank:** #{rank_global} **Country Rank:** #{rank_country} {usercountry.upper()}\n"
    embed_description +=f"▸ **PP:** {user_stats['pp']} **Acc:** {round(user_stats['acc'], 2)}%\n"
    embed_description +=f"▸ **Ranks:** {emotes['XH']} `{user_stats['xh_count']}` {emotes['X']} `{user_stats['x_count']}` {emotes['SH']} `{user_stats['sh_count']}` {emotes['S']} `{user_stats['s_count']}` {emotes['A']} `{user_stats['a_count']}`\n"
    embed_description +=f"▸ **Max Combo:** {user_stats['max_combo']}x\n"
    embed_description +=f"▸ **Level:** Not Yet\n"
    embed_description +=f"▸ **Ranked Score:** {rankedscore}\n"
    embed_description +=f"▸ **Total Score:** {totalscore}\n"
    embed_description +=f"▸ **Playcount:** {user_stats['plays']} **Playtime:** {playtime}"
    #*Userinfo Block
    #TODO: Calculate timeago on registed date
    embed_block_userinfo = f"▸ **User ID:** {user_osu['id']}\n"
    if user_discord:
        embed_block_userinfo += f"\n▸ **User Discord:** <@!{user_discord['discord_id']}>\n"
    embed_block_userinfo += f"▸ **Registed Date:** {register_date}\n"
    embed_block_userinfo += f"▸ **Last Seen Date:** {last_seen_date}\n"
    embed_block_userinfo += f"▸ **User Groups:** {userpriv}"

    #*Footer
    if user_api['action'] == None:
        additional_stuff = ""
    else:
        #?Build footer for action status, this might be pain in the ass
        additional_stuff = "| " + const.actions_statuses[int(user_api['action'])]
        if int(user_api['action']) in [2, 3, 4, 5, 12, 6, 8, 9, 10]:
            additional_stuff += f" {user_api['info_text']}"
            #*Get mods
            if int(user_api['action']) == 2:
                #*Build it
                if int(user_api['mods']) == 0:
                    mods_api = ""
                else:
                    mods_api = f"+{Mods(int(user_api['mods']))!r}"
                additional_stuff += f" {mods_api} in osu!{const.mode_names[str(user_api['mode'])].capitalize()}"
    embed_footer_1 = f"{user_api['status'][0]} {user_osu['name']} is {user_api['status'][1]}{user_api['filler1']} {user_api['activity']}ago {additional_stuff} | {glob.embed_footer}"

   #!Send Embed
    embed = discord.Embed(
        title=embed_dsc_header, 
        description=f"{embed_description}",
        color=ctx.author.color
    )
    embed.set_author(
        name=embed_header, 
        url=f"https://{glob.config.domains['main']}/u/{user_osu['id']}", 
        icon_url=f"https://{glob.config.domains['main']}/static/images/flags/{user_osu['country'].upper()}.png"
    )
    embed.set_thumbnail(
        url=f"https://{glob.config.domains['avatar']}/{userid}"
    )
    embed.add_field(
        name="User Info", 
        value=embed_block_userinfo, 
        inline=False
    )
    embed.set_footer(
        text=embed_footer_1
    )
    return await ctx.send(embed=embed)










@commands.command()
async def best(ctx, *args):
    cmd_name = "best"
    allowed_args = ["-m", "-u", "-rx", "-ap", "-n", "-g"]
    args_as_list = args

    #!Check if module & command disabled
    if glob.config.modules["osu"] == False:
        embed = discord.Embed(
            title="Error", 
            description="This module has been disabled by administrator.", 
            color=colors.embeds.red)
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    if glob.config.commands["best"] == False:
        embed = discord.Embed(
            title="Error", 
            description="This command has been disabled by administrator.", 
            color=colors.embeds.red)
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
        
    #!Check if user is restricted (role)
    if glob.config.restricted_access['best'] == False:
        #TODO: Optimize this, as for loop for just roles is stupid idea but works for now
        for role in ctx.author.roles:           #getting all roles of member
            if role.id == int(roles['restricted']):
                #! THIS CHECKS FOR ROLE, NOT PERMS
                # Perm check from osu is in config and lower part of code.
                # Under restricted_users_view_by_all and restricted_access
                embed = discord.Embed(title="Error", 
                description=f"You can't use `{prefix}{cmd_name}` because you're restricted!", 
                color=colors.embeds.red
                )
                embed.set_footer(text=glob.embed_footer)
                return await ctx.send(embed=embed)

    #!Parse arguments
    args = parseArgs(args, allowed_args)

    #*Check if first thing argument is not allowed
    if len(args_as_list) == 0:
        pass
    elif args_as_list[0] not in allowed_args:
        embed = discord.Embed(title="Error", 
        description=f"First argument is incorrect, check `{prefix}help {cmd_name}` if you need help", 
        color=colors.embeds.red
        )
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    
    #! Parse user
    if "-u" in args:
        if len(args["-u"]) > 15:
            # Max nick length on server is 15, so if it's over 15
            # it will be mention, otherwise it won't find user after all ;)

            # Cut <! and > from mention to leave id
            user = args["-u"][3:-1]
            if str(ctx.author.id) == str(user):
                self_execute = True
                desc1 = f"You don't have your osu profile linked, type `{prefix}help link` if you need help.\n You can always try with your 727 name\nRemember that names like `-u s e r-` must be put in quotation marks for example "+'`.profile -u "-u s e r-"`\n'
            else:
                self_execute = False
                desc1 = f"User not found, maybe they don't have discord connected?\n You can also try with their 727.tk username\nRemember that names like `-u s e r-` must be put in quotation marks for example "+'`.profile -u "-u s e r-"`\n'
            
            #* Database stuff
            user_discord = await glob.db.fetch(
                "SELECT osu_id, default_mode FROM discord WHERE discord_id = %s", user
            )
            
            #! User not found, in this case not linked
            if not user_discord:
                embed = discord.Embed(title="Error",
                description=f"{desc1}.\nIf you need help with this command type `{prefix}help {cmd_name}`", 
                color=colors.embeds.red)
                embed.set_footer(text=glob.embed_footer)
                return await ctx.send(embed=embed)
            
            #* Get osu info
            userid = user_discord["osu_id"]
            user_osu = await glob.db.fetch(
                "SELECT id, name, priv, country,"
                "silence_end, creation_time,"
                "latest_activity, clan_id, clan_priv "
                "FROM users WHERE id = %s", userid
            )
        else:
            # It was bancho name all along
            user = args["-u"]
            if user.startswith('"') and user.endswith('"'):
                user = user[1:-1]
            user_osu = await glob.db.fetch(
                "SELECT id, name, priv, country,"
                "silence_end, creation_time,"
                "latest_activity, clan_id, clan_priv "
                "FROM users WHERE name = %s", user
            )
            if not user_osu:
                embed = discord.Embed(title="Error",
                description=f"User not found, maybe they don't have discord connected?\n"
                             "You can also try with their 727.tk username\nRemember that " 
                             "names like `-u s e r-` must be put in quotation marks for example "
                             '`.profile -u "-u s e r-"`\n'
                             f"\nIf you need help with this command type `{prefix}help {cmd_name}`",
                color=colors.embeds.red)
                embed.set_footer(text=glob.embed_footer)
                return await ctx.send(embed=embed)
            user_oid = user_osu['id']
            user_discord = await glob.db.fetch(
                "SELECT discord_id, default_mode FROM discord WHERE osu_id = %s", user_oid
            )
            if user_discord and str(user_discord['discord_id']) == str(ctx.author.id):
                self_execute = True
            else:
                self_execute = False
    else:
        #Not specified, get author id and check if linked
        user = ctx.author.id
        self_execute = True
        
        #* Database stuff
        user_discord = await glob.db.fetch(
            "SELECT osu_id, default_mode FROM discord WHERE discord_id = %s ", user
        )
        #! User not found, in this case not linked
        if not user_discord:
            embed = discord.Embed(
                title="Error",
                description=f"You don't have your osu profile linked, type `{prefix}help link` "
                            f"if you need help.\nYou can always try with your 727 name"
                            f"\nRemember that names like `-u s e r-` must be put in quotation marks "
                            f"for example "+'`.profile -u "-u s e r-"`'
                            f"\nIf you need help with this command type `{prefix}help {cmd_name}`", 
                color=colors.embeds.red)
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed)
        
        #* Get osu info
        userid = user_discord["osu_id"]
        user_osu = await glob.db.fetch(
            "SELECT id, name, priv, country,"
            "silence_end, creation_time,"
            "latest_activity, clan_id, clan_priv "
            "FROM users WHERE id = %s", userid
        )

    userid = user_osu['id']
    #!Ż bot is uncheckable
    if user_osu['id'] == 1:
        embed = discord.Embed(
        title="Error", 
        description=f"Well, you can't check {glob.config.bancho_bot_name} on discord. For some reason it just won't work",
        color=colors.embeds.red)
        embed.set_footer(text=f"Bot Version: {version}")
        return await ctx.send(embed=embed)

    #Also make sure to get author perms !Not checked if turned off in config
    if glob.config.restricted_users_view_by_all == False:
        author_discord = await glob.db.fetch(
            "SELECT osu_id FROM discord WHERE discord_id = %s", ctx.author.id
        )
        if author_discord:
            author_oid = author_discord['osu_id']
            author_osu = await glob.db.fetch("SELECT priv FROM users WHERE id = %s", author_oid)
        else:
            author_osu = {
                "priv": 3
            }
        
        user_priv = Privileges(int(user_osu['priv']))
        author_priv = Privileges(int(author_osu['priv']))
        #! Check if restricted, if yes check if allowed in config, in no check perms, 
        #! if yes check admin commands allowed in public, if no check channel
        if Privileges.Normal not in user_priv and not glob.config.restricted_users_view_by_all:
        # user is restricted and only admins can do this, we should check if they are allowed to use it in this channel or not
            if not author_priv & Privileges.Staff:
                embed = discord.Embed(
                    title="Error", 
                    description=f"You don't have permissions to check profiles of restricted users.", 
                    color=colors.embeds.red)
                embed.set_footer(text=glob.embed_footer)
                return await ctx.send(embed=embed)

            if glob.config.restrict_admin_commands == True and str(ctx.channel.category_id) != glob.config.channels['admin_stuff']:
                embed = discord.Embed(
                    title="Error", 
                    description=f"Due to security reasons, viewing restricted people profiles is only available in admin channels", 
                    color=colors.embeds.red)
                embed.set_footer(text=glob.embed_footer)
                return await ctx.send(embed=embed)
    
    # continue as normal here if they aren't restricted/they are allowed to view profile
    #! FINALLY CHECK MODE
    if "-m" in args:
        try:
            mode = str(const.modes[args["-m"].lower()])
        except:
            embed = discord.Embed(title="Invalid Syntax", description=f"Mode is incorrect\nYou can use mode names like `mania` or `std` or mode numbers (`0-3`)\nType `{prefix}help {cmd_name}` if you need help", color=colors.embeds.red)
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed)
    else:
        #! M not specified, get it from user discord, if not existing set std
        if user_discord:
            mode = user_discord['default_mode']
        else:
            mode = "0"
#! Check rx ap and set mode corresponding to it
    # Check rx syntax
    if "-rx" in args and "-ap" in args:
        embed = discord.Embed(title="Invalid Syntax", description=f"Using both `-rx` and `-ap` is not possible\nType `{prefix}help {cmd_name}` if you need help", color=colors.embeds.red)
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    if "-rx" in args:
        if mode == "3":
            embed = discord.Embed(title="Invalid Syntax", description=f"Using `-rx` with mania is not possible\nType `{prefix}help {cmd_name}` if you need help", color=colors.embeds.red)
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed)
        else:
            # Assign mode and mods
            mode_gulag = const.rx_modes[mode]
            mode_mods = "rx"
            embed_with_mods_text = " with Relax"
    # Check ap syntax
    elif "-ap" in args:
        if mode != "0":
            embed = discord.Embed(title="Invalid Syntax", description=f"Using `-ap` in modes other than standard is not possible\nType `{prefix}help {cmd_name}` if you need help", color=colors.embeds.red)
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed)
        else:
            # Assign mode and mods
            mode_gulag = "7"
            mode_mods = "ap"
            embed_with_mods_text = " with Autopilot"
    else:
    # No mods, assign mode and mods
        mode_gulag = mode
        mode_mods = "vn"
        embed_with_mods_text = " "

    #! Online api for footer
    #! API request to get status
    #TODO: Move to aiohttp as this shit below is not async.
    response = requests.get(f"https://{glob.config.domains['api']}/api/get_player_status?id={userid}")
    json_object = json.loads(response.text)
    req = json_object["player_status"]
    
    if req['online'] == True:
        user_status = ["🟢", "Online"]
    else:
        user_status = ["🔴", "Offline"]

    #! -g argument, it also ends command here yay
    if "-g" in args:
        g = args["-g"]
        # Check if -g is a number
        try:
            g = float(g)
        except:
            embed = discord.Embed(title="Invalid Syntax", description=f"`-g` argument must be a digit\nType `{prefix}help {cmd_name}` if you need help", color=colors.embeds.red)
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed)
        finally:
            g = float(g)

        #Min pp for using -g
        if g < float(glob.config.opt_best['min_g_value']):
            await ctx.send(f"-g argument must be above {glob.config.opt_best['min_g_value']}\nAutomatically changed", delete_after=10)
            g = float(glob.config.opt_best['min_g_value'])
        
        #SQL Stuff
        if glob.config.opt_best['g_fetch_failed'] == False:
            if mode_mods == "vn":
                res = await glob.db.fetchall("SELECT COUNT(id) as `amount` FROM scores_vn WHERE pp>%s AND userid=%s AND mode=%s AND grade != 'F'", (g, userid, mode))
            if mode_mods == "rx":
                res = await glob.db.fetchall("SELECT COUNT(id) as `amount` FROM scores_rx WHERE pp>%s AND userid=%s AND mode=%s AND grade != 'F'", (g, userid, mode))
            if mode_mods == "ap":
                res = await glob.db.fetchall("SELECT COUNT(id) as `amount` FROM scores_ap WHERE pp>%s AND userid=%s AND mode=%s AND grade != 'F'", (g, userid, mode))
        else:
            if mode_mods == "vn":
                res = await glob.db.fetchall("SELECT COUNT(id) as `amount` FROM scores_vn WHERE pp>%s AND userid=%s AND mode=%s", (g, userid, mode))
            if mode_mods == "rx":
                res = await glob.db.fetchall("SELECT COUNT(id) as `amount` FROM scores_rx WHERE pp>%s AND userid=%s AND mode=%s", (g, userid, mode))
            if mode_mods == "ap":
                res = await glob.db.fetchall("SELECT COUNT(id) as `amount` FROM scores_ap WHERE pp>%s AND userid=%s AND mode=%s", (g, userid, mode))

        g_amt = res[0]['amount']

        #!Build embed    
        emb_footer = f"{user_status[0]} {user_osu['name']} is now {user_status[1].lower()} on {glob.config.servername} | {glob.embed_footer}"
        if self_execute == True:
            header_author = f"Your Bests"
            desc_prefix = "You have"
        else:
            header_author = f"{user_osu['name']}'s' Bests"
            desc_prefix = f"{user_osu['name']} has"
        embed = discord.Embed(
            title=f"", 
            description=f"▸ {desc_prefix} **{g_amt}** plays worth over **{g} PP**", 
            color=ctx.author.color)
        embed.set_author(
            name=header_author, 
            url=f"https://{glob.config.domains['main']}/u/{userid}", 
            icon_url=f"https://{glob.config.domains['main']}/static/images/flags/{user_osu['country'].upper()}.png")
        embed.set_thumbnail(url=f"https://{glob.config.domains['avatar']}/{userid}")
        embed.set_footer(text=emb_footer)
        #Send embed
        return await ctx.send(embed=embed)

    #!Define -n
    if "-n" in args:
        score_num = args["-n"]
        if score_num.isdigit() == False:
            embed = discord.Embed(title="Invalid Syntax", description=f"`-n` argument must be a digit\nType `{prefix}help {cmd_name}` if you need help", color=colors.embeds.red)
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed)
        else:
            score_num = int(score_num)
        
        if score_num < 1 or score_num > 100: #WYSI
            embed = discord.Embed(title="Invalid Syntax", description=f"`-n` argument must be a between `0` and `100`\nType `{prefix}help {cmd_name}` if you need help", color=colors.embeds.red)
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed)
    #If not spcified, set to 1
    else:
        score_num = 1
    

    #! Get scores from api
    scores = requests.get(f"https://{glob.config.domains['api']}/api/get_player_scores"
                          f"?id={userid}&scope=best&mods={mode_mods}&mode={mode_gulag}&limit={score_num}")
    json_object = json.loads(scores.text)
    scores = json_object['scores']
    fetched_score_count = len(scores)
    #! Error catching with score amount
    #* If no scores return error
    if fetched_score_count == 0:
        if self_execute == True:
            if int(mode) == 2 and glob.config.no_catch == True:
                no_catch = " (That's good, keep it like this)" 
            else:
                no_catch = ""
            embed = discord.Embed(
                title="Error", 
                description=f"You don't have any scores in {const.mode_names[str(mode)]}{embed_with_mods_text}{no_catch}", 
                color=colors.embeds.red)
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Too big", 
                description=f"{user_osu['name']} doesn't have any scores in {const.mode_names[str(mode)]}{embed_with_mods_text}", 
                color=colors.embeds.red)
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed)

    #* If -n is bigger than fetched scores return error, select last one possible but dont stop
    elif fetched_score_count != score_num:
        if self_execute == True:
            embed = discord.Embed(
                title="Too big", 
                description=f"You don't have this many scores in {const.mode_names[str(mode)]}{embed_with_mods_text}, displaying your last one (Best nr. {fetched_score_count})", 
                color=colors.embeds.purple)
            embed.set_footer(text=glob.embed_footer)
            await ctx.send(embed=embed, delete_after=10)
        else:
            embed = discord.Embed(
                title="Too big", 
                description=f"{user_osu['name']} doesn't have this many scores in {const.mode_names[str(mode)]}{embed_with_mods_text}, displaying their last one (Best nr. {fetched_score_count})", 
                color=colors.embeds.purple)
            embed.set_footer(text=glob.embed_footer)
            await ctx.send(embed=embed, delete_after=10)
        
        score_num = fetched_score_count
        score = scores.pop()
    #* Everything went good, assign score
    else:
        score = scores[int(score_num)-1]
    
    #!Build embed
    beatmap = score['beatmap']
    embed_header = ""
    # User specific message selecting
    if self_execute == True:
        embed_header += "Your"
    else:
        embed_header += f"{user_osu['name']}'s"

    # Create header
    embed_header += f" {score_num}. Best in osu!{const.mode_names[str(mode)].capitalize()}"

    # Check if rx or ap in mode, if yes add it
    if mode_mods.lower() in ["rx", "ap"]:
        embed_header += f" with {const.mods_full_names[mode_mods].capitalize()}"

    # Create header
    embed_desc_header = f"{beatmap['artist']} - {beatmap['title']} [{beatmap['version']}]"


    #This is where the fun begins
    embed_desc = f"▸ {emotes[score['grade'].upper()]} ▸ **{round(score['pp'], 2)} PP** ▸ {round(float(score['acc']), 2)}%"
    if mode == "0":
        judgements = f"[{score['n300']}/{score['n100']}/{score['n50']}/{score['nmiss']}]"
        combo = f"x{score['max_combo']}/{beatmap['max_combo']}"
        desc_3rd_line = f"▸ HP: {beatmap['hp']} ▸ OD: {beatmap['od']} ▸ CS: {beatmap['cs']} ▸ AR: {beatmap['ar']}"
    elif mode == "1":
        judgements = f"[{score['n300']}/{score['n100']}/{score['nmiss']}]"
        combo = f"x{score['max_combo']}/{beatmap['max_combo']}"
        desc_3rd_line = f"▸ HP: {beatmap['hp']} ▸ OD: {beatmap['od']} ▸ BPM: {beatmap['bpm']}"
    elif mode == "2":
        judgements = f"[{score['n300']}/{score['n100']}/{score['n50']}/{score['ngeki']}]"
        combo = f"x{score['max_combo']}/{beatmap['max_combo']}"
        desc_3rd_line = f"▸ HP: {beatmap['hp']} ▸ OD: {beatmap['od']} ▸ CS: {beatmap['cs']} ▸ AR: {beatmap['ar']}"
    elif mode == "3":
        judgements = f"[{score['ngeki']}/{score['n300']}/{score['nkatu']}/{score['n100']}/{score['n50']}/{score['nmiss']}]"
        combo = f"x{score['max_combo']}"
        embed_desc += f" ▸ **Ratio:** 1:{round(int(score['ngeki'])/int(score['n300']), 3)}"
        desc_3rd_line = f"▸ HP: {beatmap['hp']} ▸ OD: {beatmap['od']} ▸ BPM: {beatmap['bpm']}"
    
    #Create embed desc
    embed_desc += f""

    # Check for stars, if ht add arrow down, if dt or nc add arrow up if none dont add it
    if score['mods'] != 0:
        embed_desc_header += f" +{Mods(int(score['mods']))!r}"
    if Mods.HALFTIME in Mods(int(score['mods'])):
        stars = f"{round(beatmap['diff'], 2)}★▼"
    elif Mods.NIGHTCORE in Mods(int(score['mods'])) or Mods.DOUBLETIME in Mods(int(score['mods'])):
        stars = f"{round(beatmap['diff'], 2)}★▲"
    else:
        stars = f"{round(beatmap['diff'], 2)}★"
    
    # Set beatmap creator and set heard to link
    embed_desc_header += f" by {beatmap['creator']}"
    embed_desc_header = f"[{embed_desc_header}](https://osu.ppy.sh/b/{beatmap['id']})"
    
    # Add comas to score
    map_score = "{:,}".format(score['score'])
    
    # Getting time of play submit, and converting it to timeago instead of date
    time1 = datetime.datetime.utcnow()
    time2 = pandas.to_datetime(score["play_time"], format="%Y-%m-%dT%H:%M:%S")
    playtime = tu.time_ago(time1, time2)

    # Add 2 another parts of embed description
    embed_desc += f"\n▸ **{map_score}** ▸ {combo} ▸ {judgements}"
    embed_desc += f"\n{desc_3rd_line} ▸ {stars}"
    embed_desc += f"\n▸ Submitted {playtime} ago"

    # Finish description
    embed_desc = f"**{embed_desc_header}**\n{embed_desc}"

    #* Set footer
    emb_footer = f"{user_status[0]} {user_osu['name']} is now {user_status[1].lower()} on {glob.config.servername} | {glob.embed_footer}"
    #* Create embed object and send it
    embed = discord.Embed(
        title="",
        description=embed_desc,
        color=ctx.author.color
    )
    embed.set_author(
        name=embed_header,
        url=f"https://{glob.config.domains['main']}/u/{user_osu['id']}",
        icon_url=f"https://{glob.config.domains['main']}/static/images/flags/{user_osu['country'].upper()}.png"
    )
    embed.set_thumbnail(url=f"https://{glob.config.domains['avatar']}/{user_osu['id']}")
    embed.set_footer(text=emb_footer)
    await ctx.send(embed=embed)






@commands.command(aliases=["recent"])
async def rs(ctx, *args):
    """Check user most recent score"""
    allowed_args = ["-u", "-rx", "-ap", "-m"]
    cmd_name = "profile"
    args_as_list = args

    #!Check if module & command disabled
    if glob.config.modules["osu"] == False:
        embed = discord.Embed(
            title="Error", 
            description="This module has been disabled by administrator.", 
            color=colors.embeds.red)
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    if glob.config.commands["rs"] == False:
        embed = discord.Embed(
            title="Error", 
            description="This command has been disabled by administrator.", 
            color=colors.embeds.red)
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
        
    #!Check if user is restricted (role)
    if glob.config.restricted_access['rs'] == False:
        #TODO: Optimize this, as for loop for just roles is stupid idea but works for now
        for role in ctx.author.roles:           #getting all roles of member
            if role.id == int(roles['restricted']):
                #! THIS CHECKS FOR ROLE, NOT PERMS
                # Perm check from osu is in config and lower part of code.
                # Under restricted_users_view_by_all and restricted_access
                embed = discord.Embed(title="Error", 
                description=f"You can't use `{prefix}{cmd_name}` because you're restricted!", 
                color=colors.embeds.red
                )
                embed.set_footer(text=glob.embed_footer)
                return await ctx.send(embed=embed)

    #!Parse arguments
    args = parseArgs(args, allowed_args)

    #*Check if first thing argument is not allowed
    if len(args_as_list) == 0:
        pass
    elif args_as_list[0] not in allowed_args:
        embed = discord.Embed(title="Error", 
        description=f"First argument is incorrect, check `{prefix}help {cmd_name}` if you need help", 
        color=colors.embeds.red
        )
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    
    #! Parse user
    if "-u" in args:
        if len(args["-u"]) > 15:
            # Max nick length on server is 15, so if it's over 15
            # it will be mention, otherwise it won't find user after all ;)

            # Cut <! and > from mention to leave id
            user = args["-u"][3:-1]
            if str(ctx.author.id) == str(user):
                self_execute = True
                desc1 = f"You don't have your osu profile linked, type `{prefix}help link` if you need help.\n You can always try with your 727 name\nRemember that names like `-u s e r-` must be put in quotation marks for example "+'`.profile -u "-u s e r-"`\n'
            else:
                self_execute = False
                desc1 = f"User not found, maybe they don't have discord connected?\n You can also try with their 727.tk username\nRemember that names like `-u s e r-` must be put in quotation marks for example "+'`.profile -u "-u s e r-"`\n'
            
            #* Database stuff
            user_discord = await glob.db.fetch(
                "SELECT osu_id, default_mode FROM discord WHERE discord_id = %s", user
            )
            
            #! User not found, in this case not linked
            if not user_discord:
                embed = discord.Embed(title="Error",
                description=f"{desc1}.\nIf you need help with this command type `{prefix}help {cmd_name}`", 
                color=colors.embeds.red)
                embed.set_footer(text=glob.embed_footer)
                return await ctx.send(embed=embed)
            
            #* Get osu info
            userid = user_discord["osu_id"]
            user_osu = await glob.db.fetch(
                "SELECT id, name, priv, country,"
                "silence_end, creation_time,"
                "latest_activity, clan_id, clan_priv "
                "FROM users WHERE id = %s", userid
            )
        else:
            # It was bancho name all along
            user = args["-u"]
            if user.startswith('"') and user.endswith('"'):
                user = user[1:-1]
            user_osu = await glob.db.fetch(
                "SELECT id, name, priv, country,"
                "silence_end, creation_time,"
                "latest_activity, clan_id, clan_priv "
                "FROM users WHERE name = %s", user
            )
            if not user_osu:
                embed = discord.Embed(title="Error",
                description=f"User not found, maybe they don't have discord connected?\n"
                             "You can also try with their 727.tk username\nRemember that " 
                             "names like `-u s e r-` must be put in quotation marks for example "
                             '`.profile -u "-u s e r-"`\n'
                             f"\nIf you need help with this command type `{prefix}help {cmd_name}`",
                color=colors.embeds.red)
                embed.set_footer(text=glob.embed_footer)
                return await ctx.send(embed=embed)
            user_oid = user_osu['id']
            user_discord = await glob.db.fetch(
                "SELECT discord_id, default_mode FROM discord WHERE osu_id = %s", user_oid
            )
            if user_discord and str(user_discord['discord_id']) == str(ctx.author.id):
                self_execute = True
            else:
                self_execute = False
    else:
        #Not specified, get author id and check if linked
        user = ctx.author.id
        self_execute = True
        
        #* Database stuff
        user_discord = await glob.db.fetch(
            "SELECT osu_id, default_mode FROM discord WHERE discord_id = %s", user
        )
        #! User not found, in this case not linked
        if not user_discord:
            embed = discord.Embed(
                title="Error",
                description=f"You don't have your osu profile linked, type `{prefix}help link` "
                            f"if you need help.\nYou can always try with your 727 name"
                            f"\nRemember that names like `-u s e r-` must be put in quotation marks "
                            f"for example "+'`.profile -u "-u s e r-"`'
                            f"\nIf you need help with this command type `{prefix}help {cmd_name}`", 
                color=colors.embeds.red)
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed)
        
        #* Get osu info
        userid = user_discord["osu_id"]
        user_osu = await glob.db.fetch(
            "SELECT id, name, priv, country,"
            "silence_end, creation_time,"
            "latest_activity, clan_id, clan_priv "
            "FROM users WHERE id = %s", userid
        )

    userid = user_osu['id']
    #!Ż bot is uncheckable
    if user_osu['id'] == 1:
        embed = discord.Embed(
        title="Error", 
        description=f"Well, you can't check {glob.config.bancho_bot_name} on discord. For some reason it just won't work",
        color=colors.embeds.red)
        embed.set_footer(text=f"Bot Version: {version}")
        return await ctx.send(embed=embed)

    #Also make sure to get author perms !Not checked if turned off in config
    if glob.config.restricted_users_view_by_all == False:
        author_discord = await glob.db.fetch(
            "SELECT osu_id FROM discord WHERE discord_id = %s", ctx.author.id
        )
        if author_discord:
            author_oid = author_discord['osu_id']
            author_osu = await glob.db.fetch("SELECT priv FROM users WHERE id = %s", author_oid)
        else:
            author_osu = {
                "priv": 3
            }
        
        user_priv = Privileges(int(user_osu['priv']))
        author_priv = Privileges(int(author_osu['priv']))
        #! Check if restricted, if yes check if allowed in config, in no check perms, 
        #! if yes check admin commands allowed in public, if no check channel
        if Privileges.Normal not in user_priv and not glob.config.restricted_users_view_by_all:
        # user is restricted and only admins can do this, we should check if they are allowed to use it in this channel or not
            if not author_priv & Privileges.Staff:
                embed = discord.Embed(
                    title="Error", 
                    description=f"You don't have permissions to check profiles of restricted users.", 
                    color=colors.embeds.red)
                embed.set_footer(text=glob.embed_footer)
                return await ctx.send(embed=embed)

            if glob.config.restrict_admin_commands == True and str(ctx.channel.category_id) != glob.config.channels['admin_stuff']:
                embed = discord.Embed(
                    title="Error",
                    description=f"Due to security reasons, viewing restricted people profiles is only available in admin channels",
                    color=colors.embeds.red)
                embed.set_footer(text=glob.embed_footer)
                return await ctx.send(embed=embed)

    # continue as normal here if they aren't restricted/they are allowed to view profile
    #! FINALLY CHECK MODE
    if "-m" in args:
        try:
            mode = str(const.modes[args["-m"].lower()])
        except:
            embed = discord.Embed(title="Invalid Syntax", description=f"Mode is incorrect\nYou can use mode names like `mania` or `std` or mode numbers (`0-3`)\nType `{prefix}help {cmd_name}` if you need help", color=colors.embeds.red)
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed)
    else:
        #! M not specified, get it from user discord, if not existing set std
        if user_discord:
            mode = user_discord['default_mode']
        else:
            mode = "0"

#! Check rx ap and set mode corresponding to it
    # Check rx syntax
    if "-rx" in args and "-ap" in args:
        embed = discord.Embed(title="Invalid Syntax", description=f"Using both `-rx` and `-ap` is not possible\nType `{prefix}help {cmd_name}` if you need help", color=colors.embeds.red)
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    if "-rx" in args:
        if mode == "3":
            embed = discord.Embed(title="Invalid Syntax", description=f"Using `-rx` with mania is not possible\nType `{prefix}help {cmd_name}` if you need help", color=colors.embeds.red)
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed)
        else:
            # Assign mode and mods
            mode_gulag = const.rx_modes[mode]
            mode_mods = "rx"
            embed_with_mods_text = " with Relax"
    # Check ap syntax
    elif "-ap" in args:
        if mode != "0":
            embed = discord.Embed(title="Invalid Syntax", description=f"Using `-ap` in modes other than standard is not possible\nType `{prefix}help {cmd_name}` if you need help", color=colors.embeds.red)
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed)
        else:
            # Assign mode and mods
            mode_gulag = "7"
            mode_mods = "ap"
            embed_with_mods_text = " with Autopilot"
    else:
    # No mods, assign mode and mods
        mode_gulag = mode
        mode_mods = "vn"
        embed_with_mods_text = " "

    #! Online api for footer
    #! API request to get status
    #TODO: Move to aiohttp as this shit below is not async.
    response = requests.get(f"https://{glob.config.domains['api']}/api/get_player_status?id={userid}")
    json_object = json.loads(response.text)
    req = json_object["player_status"]
    
    if req['online'] == True:
        user_status = ["🟢", "Online"]
    else:
        user_status = ["🔴", "Offline"]

    #! Get scores from api
    scores = requests.get(f"https://{glob.config.domains['api']}/api/get_player_scores"
                          f"?id={userid}&scope=recent&mods={mode_mods}&mode={mode_gulag}&limit=1")
    json_object = json.loads(scores.text)
    scores = json_object['scores']
    
    fetched_score_count = len(scores)
    #! Error catching with score amount
    #* If no scores return error
    if fetched_score_count == 0:
        if self_execute == True:
            if int(mode) == 2 and glob.config.no_catch == True:
                no_catch = " (That's good, keep it like this)" 
            else:
                no_catch = ""
            embed = discord.Embed(
                title="Error", 
                description=f"You don't have any scores in {const.mode_names[str(mode)]}{embed_with_mods_text}{no_catch}", 
                color=colors.embeds.red)
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Too big", 
                description=f"{user_osu['name']} doesn't have any scores in {const.mode_names[str(mode)]}{embed_with_mods_text}", 
                color=colors.embeds.red)
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed)
    else:
        score = scores[0]

    #!Build embed
    beatmap = score['beatmap']
    embed_header = ""
    # User specific message selecting
    if self_execute == True:
        embed_header += "Your"
    else:
        embed_header += f"{user_osu['name']}'s"

    # Create header
    embed_header += f" most recent score in osu!{const.mode_names[str(mode)].capitalize()}"

    # Check if rx or ap in mode, if yes add it
    if mode_mods.lower() in ["rx", "ap"]:
        embed_header += f" with {const.mods_full_names[mode_mods].capitalize()}"

    # Create header
    embed_desc_header = f"{beatmap['artist']} - {beatmap['title']} [{beatmap['version']}]"


    #This is where the fun begins
    embed_desc = f"▸ {emotes[score['grade'].upper()]} ▸ **{round(score['pp'], 2)} PP** ▸ {round(float(score['acc']), 2)}%"
    if mode == "0":
        judgements = f"[{score['n300']}/{score['n100']}/{score['n50']}/{score['nmiss']}]"
        combo = f"x{score['max_combo']}/{beatmap['max_combo']}"
        desc_3rd_line = f"▸ HP: {beatmap['hp']} ▸ OD: {beatmap['od']} ▸ CS: {beatmap['cs']} ▸ AR: {beatmap['ar']}"
    elif mode == "1":
        judgements = f"[{score['n300']}/{score['n100']}/{score['nmiss']}]"
        combo = f"x{score['max_combo']}/{beatmap['max_combo']}"
        desc_3rd_line = f"▸ HP: {beatmap['hp']} ▸ OD: {beatmap['od']} ▸ BPM: {beatmap['bpm']}"
    elif mode == "2":
        judgements = f"[{score['n300']}/{score['n100']}/{score['n50']}/{score['ngeki']}]"
        combo = f"x{score['max_combo']}/{beatmap['max_combo']}"
        desc_3rd_line = f"▸ HP: {beatmap['hp']} ▸ OD: {beatmap['od']} ▸ CS: {beatmap['cs']} ▸ AR: {beatmap['ar']}"
    elif mode == "3":
        judgements = f"[{score['ngeki']}/{score['n300']}/{score['nkatu']}/{score['n100']}/{score['n50']}/{score['nmiss']}]"
        combo = f"x{score['max_combo']}"
        embed_desc += f" ▸ **Ratio:** 1:{round(int(score['ngeki'])/int(score['n300']), 3)}"
        desc_3rd_line = f"▸ HP: {beatmap['hp']} ▸ OD: {beatmap['od']} ▸ BPM: {beatmap['bpm']}"
    
    #Create embed desc
    embed_desc += f""

    # Check for stars, if ht add arrow down, if dt or nc add arrow up if none dont add it
    if score['mods'] != 0:
        embed_desc_header += f" +{Mods(int(score['mods']))!r}"
    if Mods.HALFTIME in Mods(int(score['mods'])):
        stars = f"{round(beatmap['diff'], 2)}★▼"
    elif Mods.NIGHTCORE in Mods(int(score['mods'])) or Mods.DOUBLETIME in Mods(int(score['mods'])):
        stars = f"{round(beatmap['diff'], 2)}★▲"
    else:
        stars = f"{round(beatmap['diff'], 2)}★"
    
    # Set beatmap creator and set heard to link
    embed_desc_header += f" by {beatmap['creator']}"
    embed_desc_header = f"[{embed_desc_header}](https://osu.ppy.sh/b/{beatmap['id']})"
    
    # Add comas to score
    map_score = "{:,}".format(score['score'])
    
    # Getting time of play submit, and converting it to timeago instead of date
    time1 = datetime.datetime.utcnow()
    time2 = pandas.to_datetime(score["play_time"], format="%Y-%m-%dT%H:%M:%S")
    playtime = tu.time_ago(time1, time2)

    # Add 2 another parts of embed description
    embed_desc += f"\n▸ **{map_score}** ▸ {combo} ▸ {judgements}"
    embed_desc += f"\n{desc_3rd_line} ▸ {stars}"
    embed_desc += f"\n▸ Submitted {playtime} ago"

    # Finish description
    embed_desc = f"**{embed_desc_header}**\n{embed_desc}"

    #* Set footer
    emb_footer = f"{user_status[0]} {user_osu['name']} is now {user_status[1].lower()} on {glob.config.servername} | {glob.embed_footer}"
    #* Create embed object and send it
    embed = discord.Embed(
        title="",
        description=embed_desc,
        color=ctx.author.color
    )
    embed.set_author(
        name=embed_header,
        url=f"https://{glob.config.domains['main']}/u/{user_osu['id']}",
        icon_url=f"https://{glob.config.domains['main']}/static/images/flags/{user_osu['country'].upper()}.png"
    )
    embed.set_thumbnail(url=f"https://{glob.config.domains['avatar']}/{user_osu['id']}")
    embed.set_footer(text=emb_footer)
    await ctx.send(embed=embed)

