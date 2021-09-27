import discord
from discord.ext import commands

from cmyui import log, Ansi, utils
import datetime

from const.colors import colors
from const import constants as const
from const import glob

from utils import time as tu
from utils.utils import parseArgs, getUserGroupList

class account(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    

def setup(bot):
    bot.add_cog(account(bot))
    bot.add_command(link)
    bot.add_command(getuserid)


#Re define for easier usage
prefix = glob.config.prefix
version = const.version
roles = glob.config.roles
emotes = glob.config.emotes

@commands.command()
async def link(ctx, code=None):
    """Link the user with the osu account"""
    #!Delete execution command
    await ctx.message.delete()
    
    #!Simple checks
    #*If code not specified
    if code == None:
        embed = discord.Embed(title="Invalid Syntax", description=f"You must specify code\nType `{prefix}help link` if you need help, including how to get code", color=colors.embeds.red)
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    
    #*If code not a digit or len not 5
    if code.isdigit() == False:
        embed = discord.Embed(title="Invalid Syntax", description=f"Code must be 5-digit number\nType `{prefix}help link` if you need help, including how to get code", color=colors.embeds.red)
        embed.set_footer(text=f"Bot Version: {version}")
        return await ctx.send(embed=embed)
    if len(code) != 5:
        embed = discord.Embed(title="Invalid Syntax", description=f"Code must be 5-digit long, not shorter, not longer\nType `{prefix}help link` if you need help, including how to get code", color=colors.embeds.red)
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    
    #*Check if already linked
    alr = await glob.db.fetch(f"SELECT discord_id FROM discord WHERE `discord_id`='{ctx.author.id}'")
    if alr:
        embed = discord.Embed(title="Error", description=f"You're already verified, but if somehow you're not contact staff", color=colors.embeds.red)
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    
    #*Check user with matching code
    author_tag = ctx.author.name + "#" + ctx.author.discriminator
    res = await glob.db.fetch(f"SELECT osu_id, code FROM discord WHERE `code`='{code}' AND `discord_tag`='{author_tag}'")
    userid = res['osu_id']
    user_osu = await glob.db.fetch(F"SELECT name FROM users WHERE `id`='{userid}'")
    if not res:
        embed = discord.Embed(title="Error", description=f"Wrong code, maybe you made a typo?", color=colors.embeds.red)
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    try:
        await glob.db.execute(f"UPDATE discord SET `discord_id`='{ctx.author.id}' WHERE `code`='{code}' AND `discord_tag`='{author_tag}'")
    except Exception as e:
        embed = discord.Embed(title="Critical error", description=f"Weird stuff happened, contact staff", color=colors.embeds.red)
        embed.set_footer(text=glob.embed_footer)
        await ctx.send(embed=embed)
        return log(f"Error occured while executing 'link' by '{ctx.author.name}#{ctx.author.discriminator}'\nMessage: {e}", Ansi.RED)
    
    #!Everything went fine, send embed
    embed = discord.Embed(title="Account linked successfully", description=f"You linked your osu account on {glob.config.servername} `{user_osu['name']}`, ID: `{userid}`, with this discord account (<@{ctx.author.id}>)", color=colors.embeds.green)
    embed.set_footer(text=glob.embed_footer)
    await ctx.send(embed=embed)
    #!Add role
    role = ctx.guild.get_role(int(glob.config.roles['verified']))
    try:
        await ctx.author.add_roles(role)
    except:
        pass
    #!Send to log channel
    #*Log to console
    log(f"<{author_tag} ({ctx.author.id})> Linked their osu account <{user_osu['name']} ({res['osu_id']})> with discord account using code: {code}", Ansi.CYAN)
    #Send log to verificationlogs
    verlogs = ctx.guild.get_channel(int(glob.config.channels['verificationlogs']))
    embed = discord.Embed(title="User Verified", description=f"User <@{ctx.author.id}> Successfully verified with code: {code}, OSUID: {res['osu_id']}", color=colors.embeds.green)
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text=glob.embed_footer)
    return await verlogs.send(embed=embed) 


@commands.command()
async def getuserid(ctx, user=None):
    if user == None:
        return await ctx.send("Invalid syntax")
    usr = await glob.db.fetch(f"SELECT id FROM users WHERE `name`='{user}'")
    if not usr:
        return await ctx.send("User not found")
    await ctx.send(f"{user}'s id is {usr['id']}")