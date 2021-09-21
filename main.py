import discord
from discord.ext import commands

import os

from const import glob
from const import colors
from const import constants as const
from utils.time import hourTimestamp
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

@bot.event
async def on_ready():
    #=> Connect to db
    await const.db.connect(glob.config.sql)
    #=> Print out this shit ton of text
    print(f"\n{colors.green}Bot loaded successfully!{colors.end} @ {hourTimestamp()}")
    print(f"{colors.cyan}Bot Name: {colors.end}{bot.user.name}")
    print(f"{colors.cyan}Bot ID:{colors.end} {bot.user.id}\n")
    print(f"{colors.yellow}Bot created by def750 and grafika dzifors @ MIT License")
    #Yes, we use "My ego is beyond God understanding" license
    print(f"{colors.green}Website:{colors.end} https://seventwentyseven.tk")
    print(f"{colors.green}Github:{colors.end} https://github.com/seventwentyseven/rz-bot")
    print(f"{colors.green}Discord:{colors.end} https://seventwentyseven.tk")

bot.run(glob.config.token)
