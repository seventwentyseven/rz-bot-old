import discord
from discord.ext import commands

from const import glob
from const.colors import colors
from const.privileges import Privileges
from const import countries
import cmyui
import datetime


class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

prefix = glob.config.prefix
    

def setup(bot):
    bot.add_cog(admin(bot))
    bot.add_command(changecountry)

@commands.command()
async def changecountry(ctx, country:str=None, *, username:str=None):
    cmd_name = "changecountry"
    #! Permission check
    author = await glob.db.fetch(f"SELECT osu_id FROM discord WHERE discord_id={ctx.author.id}")
    if not author:
        embed = discord.Embed(
            title="Error", 
            description=f"You don't have your {glob.config.servername} account linked, type `{prefix}help link` if you need help",
            color=colors.embeds.red)
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    else:
        author_oid = author['osu_id']
        author_priv = await glob.db.fetch(f'SELECT priv FROM users WHERE id={author_oid}')
        author_priv = Privileges(int(author_priv['priv']))
        if Privileges.Admin not in author_priv or Privileges.Dangerous not in author_priv:
            embed = discord.Embed(
                title="Error", 
                description=f"You don't have permissions to execute this command",
                color=colors.embeds.red)
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed) 
    #! Syntax check
    if country == None or username == None:
        embed = discord.Embed(
            title="Error", 
            description=f"Invalid syntax, type `{prefix}help {cmd_name}` if you need help",
            color=colors.embeds.red)
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)

    if country.lower() not in countries.country_codes:
        embed = discord.Embed(
            title="Error", 
            description=f"Country not found, if you don't know the country code, just google it",
            color=colors.embeds.red)
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    
    # Select username
    res = await glob.db.fetch(f"SELECT id, name, country FROM users WHERE `name`='{username}'")
    if not res:
        embed = discord.Embed(
            title="Error", 
            description=f"Username not found",
            color=colors.embeds.red)
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    
    #! Everything went fine
    userid = res['id']
    await glob.db.execute(f"UPDATE `users` SET `country`='{country.upper()}' WHERE `id`='{userid}'")
    embed = discord.Embed(
        title="Country Changed", 
        description=f"Successfully changed {res['name']} (ID {res['id']}) country from `{res['country'].upper()}` to `{country.upper()}`",
        color=colors.embeds.green)
    embed.set_footer(text=glob.embed_footer)
    return await ctx.send(embed=embed)