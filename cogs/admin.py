from re import A
import discord
from discord.ext import commands

from const import glob
from const.colors import colors
from const.privileges import Privileges
from const import countries
from utils.utils import parseArgs

import cmyui
import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

prefix = glob.config.prefix


def setup(bot):
    bot.add_cog(admin(bot))
    bot.add_command(changecountry)
    bot.add_command(sendtemplate)
    bot.add_command(givedonator)

@commands.guild_only()
@commands.command()
async def changecountry(ctx, country:str=None, *, username:str=None):
    cmd_name = "changecountry"

    #Check if module and command are enabled
    if glob.config.modules['admin'] == False:
        embed = discord.Embed(
            title="Error",
            description=f"Admin module has been disabled by administrator",
            color=colors.embeds.red
        )
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    if glob.config.commands['changecountry'] == False:
        embed = discord.Embed(
            title="Error",
            description=f"{cmd_name.capitalize()} command has been disabled by administrator",
            color=colors.embeds.red
        )
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)

    #! Permission check
    author = await glob.db.fetch("SELECT osu_id FROM discord WHERE discord_id = %s", ctx.author.id)
    if not author:
        embed = discord.Embed(
            title="Error",
            description=f"You don't have your {glob.config.servername} account linked, We somehow need to check your perms. Type `{prefix}help link` if you need help",
            color=colors.embeds.red)
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    else:
        author_priv = await glob.db.fetch('SELECT priv FROM users WHERE id = %s', author['osu_id'])
        author_priv = Privileges(int(author_priv['priv']))
        print(author_priv)
        if Privileges.Admin not in author_priv:
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
    res = await glob.db.fetch("SELECT id, name, country FROM users WHERE name = %s", username)
    if not res:
        embed = discord.Embed(
            title="Error",
            description=f"Username not found",
            color=colors.embeds.red)
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)

    #! Everything went fine
    userid = res['id']
    await glob.db.execute("UPDATE `users` SET country = %s WHERE id = %s", (country.upper(), userid))
    embed = discord.Embed(
        title="Country Changed",
        description=f"Successfully changed {res['name']} (ID {res['id']}) country from `{res['country'].upper()}` to `{country.upper()}`",
        color=colors.embeds.green)
    embed.set_footer(text=glob.embed_footer)
    return await ctx.send(embed=embed)
@changecountry.error
async def nodms_error(ctx, error):
    if isinstance(error, commands.NoPrivateMessage):
        embed = discord.Embed(
            title="Error",
            description="This command cannot be used in DMs.",
            color=colors.embeds.red)
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)

@commands.guild_only()
@commands.command()
async def sendtemplate(ctx, *args):
    cmd_name = "sendmail"
    allowed_args = ["-u", "-template", "-list"]
    args_as_list = args

    #Check if module and command are enabled
    if glob.config.modules['mailer'] == False:
        embed = discord.Embed(
            title="Error",
            description=f"Mailer module has been disabled by administrator",
            color=colors.embeds.red
        )
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    if glob.config.commands['sendtemplate'] == False:
        embed = discord.Embed(
            title="Error",
            description=f"{cmd_name.capitalize()} command has been disabled by administrator",
            color=colors.embeds.red
        )
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)

    #Check channel
    if glob.config.restrict_admin_commands == True and str(ctx.channel.category_id) != glob.config.channels['admin_stuff']:
        embed = discord.Embed(
            title="Error",
            description=f"Due to security reasons, usage of this command is only allowed in admin channels",
            color=colors.embeds.red)
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    #Get author perms
    author = await glob.db.fetch("SELECT osu_id FROM discord WHERE discord_id=%s", ctx.author.id)
    if not author:
        embed = discord.Embed(
            title="Error",
            description=f"You don't have your {glob.config.servername} account linked, We somehow need to check your perms. Type `{prefix}help link` if you need help",
            color=colors.embeds.red
        )
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    else:
        author_priv = await glob.db.fetch("SELECT priv FROM users WHERE id=%s", author['osu_id'])
        author_priv = Privileges(int(author_priv['priv']))
        if Privileges.Admin not in author_priv:
            embed = discord.Embed(
                title="Error",
                description=f"You don't have permissions to execute this command",
                color=colors.embeds.red
            )
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed)

    #Check for first arg
    if len(args_as_list) == 1 and args_as_list[0] not in allowed_args:
        embed = discord.Embed(
            title="Invalid syntax",
            description=f"If you need help type `{prefix}help {cmd_name}`",
            color=colors.embeds.red
        )
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)

    #Parse args
    args = parseArgs(args, allowed_args)

    #Check if executioner wants to see template list
    if "-list" in args:
        embed = discord.Embed(
            title="Template list",
            description=f"List of all avaible templates: ",
            color=ctx.author.color)
        for i in glob.config.mailtemplates.keys():
            embed.description += f"`{i}` "
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)

    if "-template" in args:
        #Check if template exists
        if args["-template"].lower() not in glob.config.mailtemplates:
            embed = discord.Embed(
                title="Error",
                description=f"If you want to see aviable templates, type `{prefix}{cmd_name} -list`",
                color=colors.embeds.red
            )
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed)
        template = glob.config.mailtemplates[args["-template"]]

    else:
        embed = discord.Embed(
            title="Invalid syntax",
            description=f"You forgot about `-template` argument.\nIf you need help type `{prefix}help {cmd_name}`",
            color=colors.embeds.red
        )
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)

    if "-u" in args:
        #Check if in quotes, (weird usernames)
        if args["-u"].startswith('"') and args["-u"].endswith('"'):
            user = args["-u"][1:-1]
        else:
            user = args['-u']

        #Fetch from db
        user = await glob.db.fetch("SELECT id, name, email FROM users WHERE name=%s", user)
        if not user:
            embed = discord.Embed(
                title="Invalid syntax",
                description=f"Specified user doesn't exist in database. Maybe you made a typo?\n"
                "Remember that if username looks like this `- u s e r -` you must specify it in qutes "
                "like that:" + ' `-u "-u s e r -"`',
                color=colors.embeds.red
            )
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed)

        # If user has discord connected also get it
        user_discord = await glob.db.fetch("SELECT discord_id FROM discord WHERE osu_id=%s", user['id'])
        if not user_discord:
            user_discord = False

    else:
        embed = discord.Embed(
            title="Invalid syntax",
            description=f"You forgot about `-u` argument.\nIf you need help type `{prefix}help {cmd_name}`",
            color=colors.embeds.red
        )
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)

    #Send email and embed (if discord connected)
    #Try to send embed
    if user_discord != False:
        try:
            embed = discord.Embed(
                title=template['title'],
                description = template['email_content'].replace("<br>", "\n"),
                color=colors.embeds.red
            )
            embed.set_footer(text=glob.embed_footer)
            #get user
            user_object_d = glob.bot.get_user(int(user_discord['discord_id']))
            await user_object_d.send(embed=embed)
        except:
            embed = discord.Embed(
                title="Error",
                description=f"Cannot send message on DMs, trying to send email only",
                color=colors.embeds.red
            )
            embed.set_footer(text=glob.embed_footer)
            await ctx.send(embed=embed)

    #Try to send email
    message = Mail(
    from_email=template['email_used'],
    to_emails=user['email'],
    subject=template['title'],
    html_content=template['email_content'])
    try:
        sg = SendGridAPIClient(glob.config.sg_apikey)
        response = sg.send(message)
        cmyui.log(f"{ctx.author.name}#{ctx.author.discriminator} issued .sendtemplate,"
                  f"template used: {args['-template'].lower()}, Status code: {response.status_code}", cmyui.Ansi.YELLOW)
    except Exception as e:
        print(e.message)
        embed = discord.Embed(
            title="Error",
            description=f"Error occured while sending an email.\n**Error message:** `{e.message}`",
            color=colors.embeds.red,
        )
        if response.status_code:
            embed.description += f"\n**Status Code:** {response.status_code}"
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    finally:
        if user_discord != False:
            tag = f" ({user_object_d.name}#{user_object_d.discriminator})"
        else:
            tag = ""
        embed = discord.Embed(
            title="Email sent successfully",
            description=f"**Email used:** {template['email_used']}\n"
                        f"**Receiver:** {user['name']}{tag}\n"
                        f"**Template used**: {args['-template'].lower()}\n"
                        f"**Email title:** {template['title']}\n"
                        f"**Email content:** ```{template['email_content']}```".replace('<br>', '\n')
            ,color=colors.embeds.green,
        )
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
@sendtemplate.error
async def nodms_error(ctx, error):
    if isinstance(error, commands.NoPrivateMessage):
        embed = discord.Embed(
            title="Error",
            description="This command cannot be used in DMs.",
            color=colors.embeds.red)
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
#################################################################################################
@commands.guild_only()
@commands.command()
async def givedonator(ctx, user:str=None, time:str=None, _type:str=None):
    cmd_name = "givedonator"
    #Check if module and command are enabled
    if glob.config.modules['admin'] == False:
        embed = discord.Embed(
            title="Error",
            description=f"Admin module has been disabled by administrator",
            color=colors.embeds.red
        )
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    if glob.config.commands['givedonator'] == False:
        embed = discord.Embed(
            title="Error",
            description=f"{cmd_name.capitalize()} command has been disabled by administrator",
            color=colors.embeds.red
        )
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)

    #Get author perms
    author = await glob.db.fetch("SELECT osu_id FROM discord WHERE discord_id=%s", ctx.author.id)
    if not author:
        embed = discord.Embed(
            title="Error",
            description=f"You don't have your {glob.config.servername} account linked, We somehow need to check your perms. Type `{prefix}help link` if you need help",
            color=colors.embeds.red
        )
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    else:
        author_priv = await glob.db.fetch("SELECT priv FROM users WHERE id=%s", author['osu_id'])
        author_priv = Privileges(int(author_priv['priv']))
        if Privileges.Dangerous not in author_priv:
            embed = discord.Embed(
                title="Error",
                description=f"You don't have permissions to execute this command",
                color=colors.embeds.red
            )
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed)

    #Check user
    if user == None:
        embed = discord.Embed(
            title="Error",
            description=f"You must specify user, type `{prefix}help {cmd_name}` to get help for this command",
            color=colors.embeds.red
        )
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    else:
        if user.startswith('"') and user.endswith('"'):
            user = user[1:-1]

        #Fetch user
        user = await glob.db.fetch("SELECT id, name, priv, donor_end FROM users WHERE name=%s", user)
        if not user:
            embed = discord.Embed(
                title="Error",
                description=f"User not found, if it has spaces, put in in quotes like that" + '`"def 750"`',
                color=colors.embeds.red
            )
            embed.set_footer(text=glob.embed_footer)
            return await ctx.send(embed=embed)

    # Get donator length
    if time == None:
        await ctx.send("Time not specified, setting to 30 days", delete_after=10)
        time = 30
    #Syntax checks
    elif not time.isdigit():
        embed = discord.Embed(
            title="Error",
            description=f"Time (in days) argument must be a digit.\nType `{prefix}help {cmd_name}` to get help for this command.",
            color=colors.embeds.red
        )
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)
    #Convert to int
    else:
        time = int(time)

    #Make timedelta, what next? maybe timeepsilon and timegamma (mania refernece, why did i put this in code)
    timedelta = datetime.timedelta(days=time)
    #Now
    now = datetime.datetime.utcnow()

    #Check if had donator or has one
    if datetime.datetime.fromtimestamp(user['donor_end']) < now:
        end = now + timedelta
    else:
        donor_end = datetime.datetime.fromtimestamp(user['donor_end'])
        end = donor_end + timedelta
    end = datetime.datetime.timestamp(end)
    changed = False
    #Calculate privileges
    user_priv = Privileges(int(user['priv']))
    if _type == None:
        if Privileges.Supporter not in user_priv:
            user_priv += Privileges.Supporter
            changed = True
        type_name = "supporter"
    elif _type.lower() in ["supporterp", "supporterplus", "donatorp", "premium", "supporter+"]:
        if Privileges.Supporter not in user_priv:
            user_priv += Privileges.Supporter
            changed = True
        if Privileges.Premium not in user_priv:
            user_priv += Privileges.Premium
            changed = True
        type_name = "premium"
    else:
        await ctx.send(f"Donor type not found, setting to normal one\nType `{prefix}help {cmd_name}` if you need help", delete_after=10)
        if Privileges.Supporter not in user_priv:
            user_priv += Privileges.Supporter
            changed = True
        type_name = "supporter"
    if changed == False:
        user_priv = user['priv']

    #Update perms
    await glob.db.execute("UPDATE users SET donor_end=%s, priv=%s WHERE id=%s", [end, user_priv, user['id']])

    embed = discord.Embed(
        title="Give donator",
        description=f"Successfully added **{time}** days of {type_name} to {user['name']}",
        color=colors.embeds.green
    )
    embed.set_footer(text=glob.embed_footer)
    cmyui.log(f"{ctx.author.name}#{ctx.author.discriminator} added {time} days of {type_name} to {user['name']}", cmyui.Ansi.GREEN)
    await ctx.send(embed=embed)
    try:
        channel = glob.bot.get_channel(int(glob.config.channels['botlogs']))
        embed = discord.Embed(
            title=f"{ctx.author.name}#{ctx.author.discriminator} used .givedonator",
            description=f"{ctx.author.name}#{ctx.author.discriminator} added {time} days of {type_name} to {user['name']}",
            color=colors.embeds.green,
            timestamp=now
        )
        embed.set_footer(text=glob.embed_footer)
        return await channel.send(embed=embed)
    except:
        return
@givedonator.error
async def nodms_error(ctx, error):
    if isinstance(error, commands.NoPrivateMessage):
        embed = discord.Embed(
            title="Error",
            description="This command cannot be used in DMs.",
            color=colors.embeds.red)
        embed.set_footer(text=glob.embed_footer)
        return await ctx.send(embed=embed)