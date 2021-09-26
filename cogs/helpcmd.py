import discord
from discord.ext import commands

from const.privileges import Privileges
from const import helpresponses
from const import colors
from const import glob
from const.constants import version  as constant_version


class helpcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
#Re define for easier usage
prefix = glob.config.prefix
version = constant_version
roles = glob.config.roles
emotes = glob.config.emotes
colors = colors.colors
def setup(bot):
    bot.add_cog(helpcmd(bot))
    bot.remove_command("help")
    bot.add_command(help)

@commands.command()
async def help(ctx, cmd_name:str = "None"):
    admin_commands = ["rlc", "load", "sendmail", "sendtemplate", "checknotes"]
    # If user is trying to get help for admin command
    priv = 1
    if cmd_name.lower() in admin_commands or cmd_name == "None":
        authordisocrd = await glob.db.fetch(f"SELECT osu_id FROM discord WHERE `discord_id`='{ctx.author.id}'")
        if not authordisocrd:
            priv = 1
        else:
            userid = authordisocrd['osu_id']
            user = await glob.db.fetch(f"SELECT priv FROM users WHERE id='{userid}'")
            priv = user['priv']
    priv = Privileges(int(priv))

    #Main Help command (no args)
    if cmd_name == "None":
        embed = discord.Embed(
            title="Help - List of commands",
            description=f"Current prefix: `{prefix}`  List of commands:\n\n"
                        "**Osu:** `profile`, `rs`, `best`, `getuserid`\n"
                        "**Verification:** `link`\n",
            color=colors.embeds.blue,
        )
        #Help admin section
        if Privileges.Mod in priv or Privileges.Dangerous in priv or Privileges.Admin in priv:
            embed.description += "**Admin:** `rlc`, `load`"
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    
    # If args were specified, check if they exist
    try:
        cmd = helpresponses.helpresponses[cmd_name.lower()]
    except:
        # Command (arg) not found
        embed = discord.Embed(
            title="Error",
            description=f"Command not found, type `{prefix}help` to command list\nType `{prefix}help <command name>` to get list of commands",
            color=colors.embeds.red,
        )
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    finally:
        # Return embed with command help
        #! No perms
        if cmd_name in admin_commands and cmd['privileges'] not in priv:
            embed = discord.Embed(
                title="Error",
                description=f"Command not found, type `{prefix}help` to command list\nType `{prefix}help <command name>` to get list of commands",
                color=colors.embeds.red,
            )
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed)

        # Everything went smooth and fine, return command's help
        embed = discord.Embed(
            title=f"Help command - {cmd['header']}",
            description=f"**{cmd['description']}**\n**Example usage:** {cmd['example']}\n{cmd['info']}",
            color=colors.embeds.blue,
        )
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
