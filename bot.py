import discord
import json
import os
import sys

from discord.ext import commands
from cogs.utils import checks

# description showed when you use the help command
description = 'test'

# sets up the bots characteristics.
# command_prefix is the character used before commands
help_attrs = dict(hidden=True)
bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'),
                   description=description,
                   pm_help=None,
                   help_attrs=help_attrs)

settings = None

# a quick thing i made to look in a cogs folder and save all extensions in
# the list


def list_cogs():
    return ['cogs.' + i.replace('/', '\\').split('\\')[0][:-3] for i in os.listdir('cogs') if i.endswith('.py')]


def load_cog(cog):
    try:
        bot.load_extension(cog)
        print('Loaded {0}'.format(cog))
    except Exception as e:
        print('Failed to load cog {0}\n{1}: {2}'.format(
            cog, type(e).__name__, e))


def load_settings(settings_file="settings.json"):
    """Loads the settings"""
    global settings
    original_settings = {"owner": 123456789,
                         "password": "password", "email": "email"}

    if settings_file not in os.listdir("."):
        json.dump(original_settings, open("settings.json", "w"),
                  indent=4, sort_keys=True)
        print("Please stop the bot, edit the settings.json file, and start the bot again please :)")
        input()
        sys.exit()
    else:
        settings = json.load(open(settings_file))


@bot.command(name='exit')
@checks.is_owner()
async def exit():
    await bot.say("cya")
    await bot.logout()



# event for when the bot starts
@bot.event
async def on_ready():
    print('------')
    print('Username: ' + bot.user.name)
    print('ID: ' + bot.user.id)
    print('------')

    # this can load the cogs/extensions
    for cog in list_cogs():
        load_cog(cog)


# runs whenever someone sends a message
@bot.event
async def on_message(message):
    await bot.process_commands(message)


# this runs when someone runs a command
@bot.event
async def on_command(command, ctx):

    message = ctx.message
    destination = None
    if message.channel.is_private:
        destination = 'Private Message'
    else:
        destination = '#{0.channel.name} ({0.server.name})'.format(message)


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
async def list():
    """Lists all cogs"""
    await bot.say('Loaded cogs are: ' + ', '.join(list_cogs()))
    print('Loaded cogs are: ' + ', '.join(list_cogs()))

load_settings()
bot.run(settings["email"], settings["password"])
