##Checks.py

Checks is a utility file that contains checks to be used as decorators for commands.

##Code Walkthrough

```Python
from discord.ext import commands
```

Import [`commands`](https://github.com/Rapptz/discord.py/tree/async/discord/ext/commands) from the `discord.ext` directory.

Used to invoke the actual checking of command.

```Python
import config
```

Import the [`config.py`](https://github.com/PythonBuddies/main_bot/blob/master/config.py) file.

Contains the `owner` id, used for `is_owner` check.

```Python
def is_owner_check(message):
    return message.author.id == config.owner
```

Method that returns if the id of the message author is equal to the id of the bot owner.

```Python
def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message))
```

Actual decorator method that invokes the above `is_owner_check` method inside of a commands check.