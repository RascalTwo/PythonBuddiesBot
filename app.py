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
@asyncio.coroutine
def exit_cmd():
    yield from bot.say("Logging out.")
    yield from bot.logout()


# event for when the bot starts
@bot.event
@asyncio.coroutine
def on_ready():
    print('------')
    print('Username: ' + bot.user.name)
    print('ID: ' + bot.user.id)
    print('------')

    yield from bot.change_status(discord.Game(name="on Openshift"))

    # this can load the cogs/extensions
    for cog in list_cogs():
        load_cog(cog)

@bot.command(pass_context=True, name="eval")
@checks.is_owner()
@asyncio.coroutine
def _eval(ctx, *, code : str):
    code = code.strip('` ')
    python = '```Python\n{}\n```'
    result = None

    try:
        result = eval(code)
    except Exception as e:
        yield from bot.say(python.format(type(e).__name__ + ': ' + str(e)))
        return

    if asyncio.iscoroutine(result):
        result = yield from result

    yield from bot.say(python.format(result))

@bot.command(pass_context=True, name="exec")
@checks.is_owner()
@asyncio.coroutine
def _exec(ctx, *, code : str):
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
        yield from bot.say(python.format(type(e).__name__ + ': ' + str(e)))
        return

    for coro in coros:
        if asyncio.iscoroutine(coro):
            result += "\n{} - {}".format(coro, (yield from coro))

    yield from bot.say(python.format(result))

# runs whenever someone sends a message
@bot.event
@asyncio.coroutine
def on_message(message):
    yield from bot.process_commands(message)


# this runs when someone runs a command
@bot.event
@asyncio.coroutine
def on_command(_, ctx):
    message = ctx.message
    print('{0.author.name} {0.author.id} {0.channel.server.name} {0.channel.name} {0.clean_content}'.format(message))


def verify_cog_name(cog):
    return 'cogs.' + cog if not cog.startswith('cogs.') else cog


@bot.group(name='cog', pass_context=True)
@checks.is_owner()
@asyncio.coroutine
def _cog(ctx):
    """Command to work with cogs."""
    if ctx.invoked_subcommand is None:
        yield from bot.pm_help(ctx)


@_cog.command(name='load')
@checks.is_owner()
@asyncio.coroutine
def load(cog: str):
    """Loads a cog.

    Keyword arguments:
    cog -- Name of the cog
    """
    cog = verify_cog_name(cog)
    if cog not in list_cogs():
        yield from bot.say('The cog \'{0}\' could not be found.'.format(cog))
        return
    load_cog(cog)
    yield from bot.say('Loaded: {0}'.format(cog))


@_cog.command(name='unload')
@checks.is_owner()
@asyncio.coroutine
def unload(cog: str):
    """Unloads a cog.

    Keyword arguments:
    cog -- Name of the cog
    """
    cog = verify_cog_name(cog)
    bot.unload_extension(cog)
    print('Unloaded {0}'.format(cog))
    yield from bot.say('Unloaded: {0}'.format(cog))


@_cog.command(name='reload')
@checks.is_owner()
@asyncio.coroutine
def reload(cog: str):
    """Reloads a cog.

    Keyword arguments:
    cog -- Name of the cog
    """
    cog = verify_cog_name(cog)
    if cog not in list_cogs():
        yield from bot.say('The cog \'{0}\' could not be found.'.format(cog))
        return
    bot.unload_extension(cog)
    load_cog(cog)
    yield from bot.say('Reloaded: {0}'.format(cog))


@_cog.command(name='list')
@checks.is_owner()
@asyncio.coroutine
def list_cogs_cmd():
    """Lists all cogs"""
    yield from bot.say('Loaded cogs are: ' + ', '.join(list_cogs()))
    print('Loaded cogs are: ' + ', '.join(list_cogs()))

def start():
    bot.run(config.email, config.password)

if __name__ == "__main__":
    while True:
        try:
            start()
        except Exception, e:
            print e
            print e.__name__
            print "Something went wrong..."