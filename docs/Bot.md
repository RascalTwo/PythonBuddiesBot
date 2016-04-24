##Bot.py

This is the main Python script that creates the bot, loads the cogs, and runs the bot.

##Code Walkthrough

```Python
import os
```

Import [os](https://docs.python.org/3/library/os.html)

Used to load all the cogs within the `cogs/` directory.

```Python
import discord
```

Import [Discord.py](https://github.com/Rapptz/discord.py)

Used to do all the websockets and heavy lifting for us, allowing us to focus on easier tasks - mainly cogs and the fun stuff.

```Python
from discord.ext import commands
```

Import [`commands`](https://github.com/Rapptz/discord.py/tree/async/discord/ext/commands) from the `discord.ext` directory.

Used to create the bot with our description and command prefix.

```Python
from cogs.utils import checks
```

Import the [`checks`](https://github.com/PythonBuddies/main_bot/blob/master/cogs/utils/checks.py) utility file from the `cogs.utils` directory.

Used to restrict usage of certain commands to only the cog owner.

```Python
import config
```

Import the [`config.py`](https://github.com/PythonBuddies/main_bot/blob/master/config.py) file.

Contains the email and password of the account the bot will run under. Also contains the owner ID and command prefix.

*****

```Python
description = ('PyBuddies Discord bot.\nSee my code at'
               'https://www.github.com/PyBuddies/main_bot/')
```

Create a string with the description of the bot inside of it.

Is shown whenever the `!help` command of the bot is executed.

```Python
bot = commands.Bot(command_prefix=commands.when_mentioned_or(config.prefix),
                   description=description,
                   pm_help=None)
```

Create the bot, setting the command prefix, description, and help PM settings. [Up to date documentation](https://github.com/Rapptz/discord.py/blob/async/discord/ext/commands/bot.py#L126) on what all three of these mean.


Tells the bot to (1) only respond when the prefix provided - `config.prefix` is at the beginning of a message, or (2) when mentioned directly. Also provides the bot the above-set descripton. Lastly, tells the bot to only PM help messages when they're over 1000 characters.

*****

```Python
def list_cogs():
```

Create the `list_cogs` method, which returns a list of all the cogs in the `cogs` directory

Used for loading all cogs for the `list` subcommands of `cog`.

```Python
    cogs = []
````

Create the empty list which will be populated and returned when finished.

```Python
    for root, _, filenames in os.walk('cogs'):
```

Executes the [`os.walk`](https://docs.python.org/3/library/os.html#os.walk) method on the `cogs` directory, ignoring the `dirnames` variable returned.

```Python
        if root.endswith('__pycache__'):
            continue
```

Continues onto the next directory if the current directory is `__pycache__`.

```Python
        for filename in filenames:
```

For every filename in the list of filenames in the current directory.

```Python
            full_name = os.path.join(root, filename)
```

Combine the `root` and `filename` to get the full path to the file.

```Python
            if not full_name.endswith('.py'):
                continue
```

If the full path to the file does not end in `.py` - the file is not a python script - then continue onto the next file.

```Python
            if '__init__' in full_name:
                continue
```

If the full path to the file contains `__init__`, continue ontp the next file.

```Python
            if 'util' in full_name:
                continue
```

If the full path to the file contains 'util', continue ontp the next file.

```Python
            cogs.append(full_name.replace('/', '.').replace('\\', '.')[0:-3])
```

Add this cog to the list to be returned.

First replace all forward-slashes with periods, then all back-slashed with periods, and lastly remove the `.py` from the name.

```Python
    return cogs
```

Actually return the list of cogs.

*****

```Python
def load_cog():
```

Create the `load_cog` method, which will attempt to load a provided cog by name.

```Python
    try:
        bot.load_extension(cog)
        print('Loaded {0}'.format(cog))
```

Try to load the cog name provided, print the above-shown message is successful.

```Python
    except (ImportError, discord.ClientException) as e:
        print('Failed to load cog {0}\n{1}: {2}'.format(
            cog, type(e).__name__, e))
```

If the above try block failed due to a `ImportError` or a `discord.ClientException`, then print a error message, containing (1) the cog name, (2) the error type, and (3) the error.

*****

```Python
def verify_cog_name(cog):
    return 'cogs.' + cog if not cog.startswith('cogs.') else cog
```

Create the `verify_cog_name` method, which appends `cogs.` to the name of a cog if it doesn't have it.

Is the same as this:

*****
EXAMPLE CODE - NOT ACTUAL CODE
```Python
def verify_cog_name(cog):
    if not cog.startswith('cogs.'):
        return 'cogs.' + cog
    else:
        return cog
```
EXAMPLE CODE - NOT ACTUAL CODE
*****

```Python
@bot.event
async def on_ready():
```

Add this method to the `on_ready` event in the discord bot.

This will print a status message when the bot is ready, and load all cogs.

```Python
    print('――――――')
    print('Username: {0}'.format(bot.user.name))
    print('ID: {0}'.format(bot.user.id))
    print('――――――')
```

Prints out the Username and ID of the bot to the console.

```Python
    for cog in list_cogs():
        load_cog(cog)
```

Attempt to load all cogs.

*****

```Python
@bot.event
async def on_message(message):
    await bot.process_commands(message)
```

*****

Add method to the `on_message` event of the bot, making all messages heard by the bot listened to for commands.

```Python
@bot.event
async def on_command(_, ctx):
    '''Log all commands to console output.'''
    print('{0.author.name} {0.author.id} {0.channel.server.name}'
          '{0.channel.name} {0.clean_content}'.format(ctx.message))
```

Add method to the `on_command` event of the bot, outputing all commands sent to the bot to the console.

*****

```Python
@bot.command(name='exit')
@checks.is_owner()
async def exit_cmd():
```

Create the `exit` command for the bot. Restricts it's usage to only those who pass the `is_owner()` check.

> Documentation on the `.command` decorator can be found[here](https://github.com/Rapptz/discord.py/blob/async/discord/ext/commands/core.py#L628).

```Python
    await bot.say('Logging out.')
    await bot.logout()
```

Have the bot send a 'Logging Out.' message and then log out.

> Documentation on the `.say` command can be found[here](https://github.com/Rapptz/discord.py/blob/async/discord/ext/commands/bot.py#L239).

> Documentation on the `.logout` command can be found[here](https://github.com/Rapptz/discord.py/blob/async/discord/client.py#L537).

*****

```Python
@bot.group(name='cog', pass_context=True)
@checks.is_owner()
async def _cog(ctx):
```

Create a group command named `cog`, have Context passed to the method, and restrict it to users who pass the `is_owner()` check.

> Documentation on the `.group` decorator can be found[here](https://github.com/Rapptz/discord.py/blob/async/discord/ext/commands/core.py#L568).

> Documentation on the Context object can be found[here](https://github.com/Rapptz/discord.py/blob/async/discord/ext/commands/context.py#L28).

```Python
    if ctx.invoked_subcommand is None:
        await bot.pm_help(ctx)
```

If no subcommand is invoked, PM the user help for the command.

*****

```Python
@_cog.command(name='load')
@checks.is_owner()
async def load(cog):
```

Create a subcommand of the `cog` command, named `load`, and restrict it to users who pass the `is_owner()` check.

Used to load a given cog by name.

```Python
    cog = verify_cog_name(cog)
```

Add `cogs.` prefix to cog name if needed.

```Python
    load_cog(cog)
    print('Loaded {0}'.format(cog))
    await bot.say('Loaded: {0}'.format(cog))
```

Load the cog and output a message stating the cog was loaded.

*****

```Python
@_cog.command(name='unload')
@checks.is_owner()
async def unload(cog):
```

Create a subcommand of the `cog` command, named `unload`, and restrict it to users who pass the `is_owner()` check.

Used to unload a given cog by name.

```Python
    cog = verify_cog_name(cog)
```

Add `cogs.` prefix to cog name if needed.

```Python
    if cog not in list_cogs():
        await bot.say('The cog \'{0}\' could not be found.'.format(cog))
        return
```

If the cog is not loaded, then outputs a 'not found' message and returns.

```Python
    bot.unload_extension(cog)
    print('Unloaded {0}'.format(cog))
    await bot.say('Unloaded: {0}'.format(cog))
```

Unload the cog and output a message stating the cog was unloaded.

> Documentation on `unload_extension` can be found [here]()https://github.com/Rapptz/discord.py/blob/async/discord/ext/commands/bot.py#L513.

*****

```Python
@_cog.command(name='reload')
@checks.is_owner()
async def reload_cmd(cog):
```

Create a subcommand of the `cog` command, named `reload`, and restrict it to users who pass the `is_owner()` check.

Used to reload a given cog by name.

```Python
    cog = verify_cog_name(cog)
```

Add `cogs.` prefix to cog name if needed.

```Python
    if cog not in list_cogs():
        await bot.say('The cog \'{0}\' could not be found.'.format(cog))
        return
```

If the cog is not loaded, then outputs a 'not found' message and returns.

```Python
    bot.unload_extension(cog)
    bot.load_cog(cog)
    print('Reloaded {0}'.format(cog))
    await bot.say('Reloaded: {0}'.format(cog))
```

Reload the cog and output a message stating the cog was unloaded.

*****

```Python
@_cog.command(name='list')
@checks.is_owner()
async def list_cmd():
```

Create a subcommand of the `cog` command, named `list`, and restrict it to users who pass the `is_owner()` check.

```Python
    output_message = 'Loaded cogs are: ' + ', '.join(list_cogs())
    print(output_message)
    await bot.say(output_message)
```

Output a comma-seprated list of all loaded cogs.

*****

```Python
bot.run(config.email, config.password)
```

Start the bot. No lines after this are executed until the bot is finished running, making this the last line.

> Documentation for `.run` can be found [here](https://github.com/Rapptz/discord.py/blob/async/discord/client.py#L612).