import discord
from discord import http
from discord.ext import commands
from discord.ext import tasks

import aiohttp
import cmyui
from cmyui import (log, Ansi)
import datetime
import json
import os


from const import colors
from const import constants as const
from const import glob
from utils.time import hourTimestamp
#--> Welcome text
print(f"""\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
 
      ŻŻŻŻŻŻŻ 
      Ż:::::Ż 
      ŻŻŻŻŻŻŻ

ŻŻŻŻŻŻŻŻŻŻŻŻŻŻŻŻŻŻŻ     BBBBBBBBBBBBBBBBB        OOOOOOOOO     TTTTTTTTTTTTTTTTTTTTTTT
Ż:::::::::::::::::Ż     B::::::::::::::::B     OO:::::::::OO   T:::::::::::::::::::::T
Ż:::::::::::::::::Ż     B::::::BBBBBB:::::B  OO:::::::::::::OO T:::::::::::::::::::::T
Ż:::ŻŻŻŻŻŻŻŻ:::::Ż      BB:::::B     B:::::BO:::::::OOO:::::::OT:::::TT:::::::TT:::::T
ŻŻŻŻŻ     Ż:::::Ż         B::::B     B:::::BO::::::O   O::::::OTTTTTT  T:::::T  TTTTTT
        Ż:::::Ż           B::::B     B:::::BO:::::O     O:::::O        T:::::T        
       Ż:::::Ż            B::::BBBBBB:::::B O:::::O     O:::::O        T:::::T        
      Ż:::::Ż             B:::::::::::::BB  O:::::O     O:::::O        T:::::T        
     Ż:::::Ż              B::::BBBBBB:::::B O:::::O     O:::::O        T:::::T        
    Ż:::::Ż               B::::B     B:::::BO:::::O     O:::::O        T:::::T        
   Ż:::::Ż                B::::B     B:::::BO:::::O     O:::::O        T:::::T        
ŻŻŻ:::::Ż     ŻŻŻŻŻ       B::::B     B:::::BO::::::O   O::::::O        T:::::T        
Ż::::::ŻŻŻŻŻŻŻŻ:::Ż     BB:::::BBBBBB::::::BO:::::::OOO:::::::O      TT:::::::TT      
Ż:::::::::::::::::Ż     B:::::::::::::::::B  OO:::::::::::::OO       T:::::::::T      
Ż:::::::::::::::::Ż     B::::::::::::::::B     OO:::::::::OO         T:::::::::T      
ŻŻŻŻŻŻŻŻŻŻŻŻŻŻŻŻŻŻŻ     BBBBBBBBBBBBBBBBB        OOOOOOOOO           TTTTTTTTTTT  
                            {colors.colors.yellow}Version:{colors.colors.end} {glob.version}""")
print(f'{colors.colors.cyan}Loading...{colors.colors.end}\n')
#-> Set intents
intents = discord.Intents.all()
intents.members = True
#-> Define bot
bot = commands.Bot(command_prefix=glob.config.prefix, intents=intents, case_insensitive=True)

#-> Shorten shit
colors = colors.colors
version = const.version

#-> Cog loading
for filename in os.listdir('./cogs'):
    filename1 = filename
    if filename.endswith('.py'):
        print(f"{colors.yellow}Loading {filename1}...{colors.end}")
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'{colors.green}Loaded {filename1}{colors.end}')

#Assign global footer
#TODO: Move it to other place, main.py isn't best place to do it
#!REMEMBER THAT DELETING OR CHANGING BOT CREATOR IS VIOLATION OF MIT LICENSE
try:
    footers = {
        0: f"Bot Version: {version} | Bot Creator: def750#2137",
        1: f"Bot Version: {version} | On {glob.config.servername}",
        2: f"On {glob.config.servername} | Bot Version: {glob.config.servername}",
        3: f"On {glob.config.servername} Bot Version: {version} | Bot Creator: def750#2137",
        4: f"Bot Version: {version}",
        5: f"Version: {version}",
        6: f"On: {glob.config.servername}",
    }
    glob.embed_footer = footers[glob.config.footer_type]
except Exception as e:
    cmyui.log("Config error, footer type value is incorrect", Ansi.RED)
    exit()

@bot.event
async def on_ready():
    #=> Connect to db
    await const.db.connect(glob.config.sql)
    #=> Print out this shit ton of text
    print(f"\n{colors.green}Bot loaded successfully!{colors.end} @ {hourTimestamp()}")
    print(f"{colors.cyan}Bot Name: {colors.end}{bot.user.name}")
    print(f"{colors.cyan}Bot ID:{colors.end} {bot.user.id}\n")
    print(f"{colors.yellow}Bot created by def750 and grafika dzifors on MIT License")
    #Yes, we use "My ego is beyond God's understanding" license.
    print(f"{colors.green}Website:{colors.end} https://seventwentyseven.tk")
    print(f"{colors.green}Github:{colors.end} https://github.com/seventwentyseven/rz-bot")
    print(f"{colors.green}Discord:{colors.end} https://seventwentyseven.tk")
    #! Tasks
    #Start updater
    checkUpdates.start()

#!############### UPDATE CHECKER ################!#
#Updater values
class updater():
    messages_sent = 0
    version1 = version
    version2 = version
glob.updater = updater
@tasks.loop(seconds=10)#glob.config.update_check_time)
async def checkUpdates():
    if glob.config.updater_enabled == False:
        return
    cmyui.log(f"Checking for updates...", Ansi.GREEN)
    
    # Api
    async with glob.session.get("https://rz-bot.tk/api/get_latest") as r:
        resp = await r.json()
        if resp['status'] != "Success":
            return cmyui.log("Error occured while checking updates", Ansi.RED)
        
        #Assign variables
        resp = resp['version_info']
        fetched_version = cmyui.Version(int(resp['major']), int(resp['minor']), int(resp['micro']))
        glob.updater.version1 = fetched_version
        #Output
        if glob.updater.version1 == glob.updater.version2:
            cmyui.log("No new updates found.")
        else:
            cmyui.log("Update Found!", Ansi.GREEN)
            glob.updater.version2 = glob.updater.version1
            glob.updater.messages_sent = 0
            date = datetime.datetime.fromtimestamp(resp['date_released'])
            print(f"\n\n\n{colors.red}######## NEW UPDATE ########\n")
            print(f"{colors.yellow}Current Version:{colors.end} {version}")
            print(f"{colors.yellow}New Version:{colors.end} {fetched_version}")
            print(f"{colors.yellow}Date released:{colors.end} {date}")
            print(f"{colors.yellow}\nChanges:{colors.end} \n{resp['description']}")
            if resp['bugfixes'] == "True":
                print(f"\n{colors.red}This version contains bugfixes{colors.end}\n")
            if resp['security_update'] == "True":
                print(f"\n{colors.red}This version contains security updates{colors.end}\n")
            print(f"{colors.red}############################{colors.end}\n")
            
            # Send message to owners
            for user_element in glob.config.bot_owners:
                user = bot.get_user(int(user_element))
                embed = discord.Embed(
                    title=f"New {glob.config.bancho_bot_name} update just got released",
                    description=f"**Current Version:** {version}\n"
                    f"**New Version:** {fetched_version}\n"
                    f"**Date Released:** {date}\n"
                    f"**Changes**: \n{resp['description']}\n",
                    color=colors.embeds.red
                )
                if resp['bugfixes'] == "True":
                    embed.description += f"\n__**This version contains bugfixes**__\n"
                if resp['security_update'] == "True":
                    embed.description += f"\n__**This version contains security updates**__\n"
                embed.set_footer(text=glob.embed_footer)
                try:
                    await user.send(embed=embed)
                    glob.updater.messages_sent += 1
                except:
                    cmyui.log(f"Cannot send update message to {user.name}#{user.discriminator}, skipping", Ansi.RED)
#!###############################################!#

@bot.command()
async def ping(ctx):
    await ctx.send(f"Current Ping: {round(bot.latency, 1)}")

@bot.command()
async def rlc(ctx, cog):
    if str(ctx.author.id) not in glob.config.bot_owners:
        return await ctx.send("You're not an owner")
    try:
        bot.unload_extension(f'cogs.{cog}')
        bot.load_extension(f'cogs.{cog}')
        log(f"{ctx.author.name}#{ctx.author.discriminator} reloaded cog {cog}", Ansi.YELLOW)
    except Exception as e:
        log(f"{ctx.author.name}#{ctx.author.discriminator} tried to reload cog {cog} but error occured", Ansi.YELLOW)
        print(f"{colors.red}{e}{colors.end}")
        return await ctx.send(f"Error occured while reloading cog\n```{e}```", delete_after=10)
    return await ctx.send("Reloaded Cog")

@bot.command()
async def load(ctx, cog):
    if str(ctx.author.id) not in glob.config.bot_owners:
        return await ctx.send("You're not an owner")
    try:
        bot.load_extension(f'cogs.{cog}')
        log(f"{ctx.author.name}#{ctx.author.discriminator} loaded cog {cog}", Ansi.YELLOW)
    except Exception as e:
        log(f"{ctx.author.name}#{ctx.author.discriminator} tried to load cog {cog} but error occured", Ansi.YELLOW)
        print(f"{colors.red}{e}{colors.end}")
        return await ctx.send(f"Error occured while loading cog\n```{e}```", delete_after=10)
    return await ctx.send("Loaded Cog")

@bot.command(aliases=["version"])
async def _version(ctx, input_version:str=None):
    embed = discord.Embed(
        title="Bot Version", 
        description=f"**{glob.version}**", 
        color=colors.embeds.purple, 
    )
    embed.set_footer(text="Created by def750 and grafika dzifors. © Seventwentyseven.tk 2021")
    if input_version==None:
        async with glob.session.get("https://rz-bot.tk/api/get_latest") as r:
            resp = await r.json()
            resp = resp['version_info']
        date = datetime.datetime.fromtimestamp(resp['date_released'])
        embed.add_field(
            name="Version Info",
            value=f"**Date Released:** {date}\n**Changes:**\n{resp['description']}",
            inline=True
        )
        embed.add_field(
            name="Bot Info",
            value="**Github Repo:** https://github.com/seventwentyseven/rz-bot\n"
            **"Website (Not Finished):** https://rz-bot.tk",
            inline=True
        )
    else:
        if len(input_version) != 5:
            embed = discord.Embed(
                title="Invalid Syntax",
                description=f"Version Argument must be 5 character long. Example: `{glob.config.prefix}version 0.4.1`",
                color=colors.embeds.red
            )
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed)
        input_version = input_version.split(".")
        async with glob.session.get(f"https://rz-bot.tk/api/version_history?major={input_version[0]}&minor={input_version[1]}&micro={input_version[2]}") as r:
            resp = await r.json()
            if resp['status'] == "Failed":
                embed = discord.Embed(
                    title="Error",
                    description=f"Version not found in database.",
                    color=colors.embeds.red
                )
                embed.set_footer(text=glob.embed_footer)
                return await ctx.send(embed=embed)
            resp = resp['version_info']
        date = datetime.datetime.fromtimestamp(resp['date_released'])
        embed.add_field(
            name="Version Info",
            value=f"**Date Released:** {date}\n**Changes:**\n{resp['description']}",
            inline=True
        )
        embed.add_field(
            name="Bot Info",
            value="**Github Repo:** https://github.com/seventwentyseven/rz-bot\n"
            **"Website (Not Finished):** https://rz-bot.tk",
            inline=True
        )
   
    return await ctx.send(embed=embed)

#Im a fucking mastermind
glob.bot = bot

bot.run(glob.config.token)
