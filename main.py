import discord
from discord.ext import commands

import cmyui
from cmyui import (log, Ansi)
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

@bot.event
async def on_ready():
    await glob.db.connect(glob.config.sql)
    print(f"\n{colors.green}Bot loaded successfully!{colors.end} @ {hourTimestamp()}")
    print(f"{colors.cyan}Bot Name: {colors.end}{bot.user.name}")
    return print(f"{colors.cyan}Bot ID:{colors.end} {bot.user.id}")

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
async def _version(ctx):
    embed = discord.Embed(
        title="Bot Version", 
        description=f"{glob.version}", 
        color=colors.embeds.purple, 
    )
    embed.set_footer(text="Created by def750 and grafika dzifors. © Seventwentyseven.tk 2021")
    return await ctx.send(embed=embed)

bot.run(glob.config.token)
