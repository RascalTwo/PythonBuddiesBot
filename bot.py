'''PyBuddies Discord bot.

Execute this file to start the bot.

'''
import os
import discord
from discord.ext import commands
from cogs.utils import checks
import config

description = ('PyBuddies Discord bot.\nSee my code at'
               'https://www.github.com/PyBuddies/main_bot/')
bot = commands.Bot(command_prefix=commands.when_mentioned_or(config.prefix),
                   description=description,
                   pm_help=None)


def list_cogs():
    '''Return list of all cog names.

    Returns:
    list -- List of all cog names.

    '''
    cogs = []
    for root, _, filenames in os.walk('cogs'):
        if root.endswith('__pycache__'):
            continue
        for filename in filenames:
            full_name = os.path.join(root, filename)
            if not full_name.endswith('.py'):
                continue
            if '__init__' in full_name:
                continue
            if 'util' in full_name:
                continue
            cogs.append(full_name.replace('/', '.').replace('\\', '.')[0:-3])
    return cogs


def load_cog(cog):
    '''Attempt to load cog into bot.'''
    try:
        bot.load_extension(cog)
        print('Loaded {0}'.format(cog))
    except (ImportError, discord.ClientException) as e:
        print('Failed to load cog {0}\n{1}: {2}'.format(
            cog, type(e).__name__, e))


def verify_cog_name(cog):
    '''Append 'cogs.' to cog name if needed.'''
    return 'cogs.' + cog if not cog.startswith('cogs.') else cog


@bot.event
async def on_ready():
    '''Executed when the bot is ready.

    Outputs bot information and loads cods into bot.

    '''
    print('――――――')
    print('Username: {0}'.format(bot.user.name))
    print('ID: {0}'.format(bot.user.id))
    print('――――――')

    for cog in list_cogs():
        load_cog(cog)


@bot.event
async def on_message(message):
    '''Process commands within received messages.'''
    await bot.process_commands(message)


@bot.event
async def on_command(_, ctx):
    '''Log all commands to console output.'''
    print('{0.author.name} {0.author.id} {0.channel.server.name}'
          '{0.channel.name} {0.clean_content}'.format(ctx.message))

@bot.command(name='exit')
@checks.is_owner()
async def exit_cmd():
    '''Log the bot out.

    Executing user must be owner.

    '''
    await bot.say('Logging out.')
    await bot.logout()


@bot.group(name='cog', pass_context=True)
@checks.is_owner()
async def _cog(ctx):
    '''Main Command to work with cogs.'''
    if ctx.invoked_subcommand is None:
        await bot.pm_help(ctx)


@_cog.command(name='load')
@checks.is_owner()
async def load(cog):
    '''Load a cog.

    Keyword arguments:
    cog -- Name of the cog
    '''
    cog = verify_cog_name(cog)
    load_cog(cog)
    print('Loaded {0}'.format(cog))
    await bot.say('Loaded: {0}'.format(cog))


@_cog.command(name='unload')
@checks.is_owner()
async def unload(cog):
    '''Unload a cog.

    Keyword arguments:
    cog -- Name of the cog
    '''
    cog = verify_cog_name(cog)
    if cog not in list_cogs():
        await bot.say('The cog \'{0}\' could not be found.'.format(cog))
        return
    bot.unload_extension(cog)
    print('Unloaded {0}'.format(cog))
    await bot.say('Unloaded: {0}'.format(cog))


@_cog.command(name='reload')
@checks.is_owner()
async def reload_cmd(cog):
    '''Reload a cog.

    Keyword arguments:
    cog -- Name of the cog
    '''
    cog = verify_cog_name(cog)
    if cog not in list_cogs():
        await bot.say('The cog \'{0}\' could not be found.'.format(cog))
        return
    bot.unload_extension(cog)
    load_cog(cog)
    print('Reloaded {0}'.format(cog))
    await bot.say('Reloaded: {0}'.format(cog))


@_cog.command(name='list')
@checks.is_owner()
async def list_cmd():
    '''List all cogs.'''
    output_message = 'Loaded cogs are: ' + ', '.join(list_cogs())
    await bot.say(output_message)
    print(output_message)

bot.run(config.email, config.password)
