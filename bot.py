import os
import discord
from discord.ext import commands
import config
from cogs.utils import checks
import sys
from io import StringIO
import asyncio
# description showed when you use the help command
description = 'test'

# sets up the bots characteristics.
# command_prefix is the character used before commands
help_attrs = dict(hidden=True)
bot = commands.Bot(command_prefix=commands.when_mentioned_or(config.prefix),
                   description=description,
                   pm_help=None,
                   help_attrs=help_attrs)


# Slightly longer method to find cogs recursively in the cogs folder
def list_cogs():
    cogs = []
    for root, _, filenames in os.walk('cogs'):
        for filename in filenames:
            full_name = os.path.join(root, filename)
            if full_name.endswith('.py') and all(word not in full_name for word in ['pycache', "__init__", "util"]):
                cogs.append(full_name.replace('/', '.').replace('\\', '.')[0:-3])
    return cogs

def load_cog(cog):
    try:
        bot.load_extension(cog)
        print('Loaded {0}'.format(cog))
    except (ImportError, discord.ClientException) as e:
        print('Failed to load cog {0}\n{1}: {2}'.format(
            cog, type(e).__name__, e))

@bot.command(name='exit')
@checks.is_owner()
async def exit_cmd():
    await bot.say("Logging out.")
    await bot.logout()


# event for when the bot starts
@bot.event
async def on_ready():
    print('------')
    print('Username: ' + bot.user.name)
    print('ID: ' + bot.user.id)
    print('------')

    await bot.change_status(discord.Game(name="with the Discord API"))

    # this can load the cogs/extensions
    for cog in list_cogs():
        load_cog(cog)

@bot.command(pass_context=True, name="eval")
@checks.is_owner()
async def _eval(ctx, *, code : str):
    code = code.strip('` ')
    python = '```Python\n{}\n```'
    result = None

    try:
        result = eval(code)
    except Exception as e:
        await bot.say(python.format(type(e).__name__ + ': ' + str(e)))
        return

    if asyncio.iscoroutine(result):
        result = await result

    await bot.say(python.format(result))

@bot.command(pass_context=True, name="exec")
@checks.is_owner()
async def _exec(ctx, *, code : str):
    code = code.strip('` ')
    python = '```Python\n{}\n```'
    result = None
    coros = []
    try:
        result = StringIO()
        sys.stdout = result
        exec(compile(code.replace("Python", ""), "<string>", "exec"))
        result = result.getvalue()
        sys.stdout = sys.__stdout__
    except Exception as e:
        await bot.say(python.format(type(e).__name__ + ': ' + str(e)))
        return

    for coro in coros:
        if asyncio.iscoroutine(coro):
            result += "\n{} - {}".format(coro, await coro)

    await bot.say(python.format(result))

# runs whenever someone sends a message
@bot.event
async def on_message(message):
    await bot.process_commands(message)


# this runs when someone runs a command
@bot.event
async def on_command(_, ctx):
    message = ctx.message
    print('{0.author.name} {0.author.id} {0.channel.server.name} {0.channel.name} {0.clean_content}'.format(message))


def verify_cog_name(cog: str) -> str:
    return 'cogs.' + cog if not cog.startswith('cogs.') else cog


@bot.group(name='cog', pass_context=True)
@checks.is_owner()
async def _cog(ctx):
    """Command to work with cogs."""
    if ctx.invoked_subcommand is None:
        await bot.pm_help(ctx)


@_cog.command(name='load')
@checks.is_owner()
async def load(cog: str):
    """Loads a cog.

    Keyword arguments:
    cog -- Name of the cog
    """
    cog = verify_cog_name(cog)
    if cog not in list_cogs():
        await bot.say('The cog \'{0}\' could not be found.'.format(cog))
        return
    load_cog(cog)
    await bot.say('Loaded: {0}'.format(cog))


@_cog.command(name='unload')
@checks.is_owner()
async def unload(cog: str):
    """Unloads a cog.

    Keyword arguments:
    cog -- Name of the cog
    """
    cog = verify_cog_name(cog)
    bot.unload_extension(cog)
    print('Unloaded {0}'.format(cog))
    await bot.say('Unloaded: {0}'.format(cog))


@_cog.command(name='reload')
@checks.is_owner()
async def reload(cog: str):
    """Reloads a cog.

    Keyword arguments:
    cog -- Name of the cog
    """
    cog = verify_cog_name(cog)
    if cog not in list_cogs():
        await bot.say('The cog \'{0}\' could not be found.'.format(cog))
        return
    bot.unload_extension(cog)
    load_cog(cog)
    await bot.say('Reloaded: {0}'.format(cog))


@_cog.command(name='list')
@checks.is_owner()
async def list_cogs_cmd():
    """Lists all cogs"""
    await bot.say('Loaded cogs are: ' + ', '.join(list_cogs()))
    print('Loaded cogs are: ' + ', '.join(list_cogs()))

bot.run(config.email, config.password)
