##Chat.py

Contains all chat-related commands and features.

##Code Walkthrough

```Python
import random
```

Import [random](https://docs.python.org/3/library/random.html).

Used to choose between options at random.

```Python
from discord.ext import commands
```

Import [`commands`](https://github.com/Rapptz/discord.py/tree/async/discord/ext/commands) from the `discord.ext` directory.

Used to create commands for the bot.

```Python
from datetime import datetime
```

Import [datetime](https://docs.python.org/3/library/datetime.html).

Used for the timezone command.

```Python
from pytz import timezone
```

Import [pytz](https://github.com/newvem/pytz).

Used for timezone command, specifically in converting local timezones to other timezones.

```Python
from tzlocal import get_localzone
```

Import [tzlocal](https://github.com/regebro/tzlocal).

Another package for the timezone command.

```Python
from chatterbot import ChatBot
```

Import [chatterbot](https://github.com/gunthercox/ChatterBot).

Used to speak to an instance of Chatterbot.

```Python
from translate import Translator
```

Import [translate](https://github.com/terryyin/google-translate-python).

Used to translate text from english to other languages.

```Python
import wikiquote
```

Import [wikiquote](https://github.com/federicotdn/python-wikiquotes).

Used to return quotes either being random or of today.

```Python
class Chat(object):
    def __init__(self, bot):
        self.bot = bot
        self.chatbot = ChatBot("Ron Obvious")
        self.chatbot.train("chatterbot.corpus.english")
```

Create the `Chat` class and `__init__` method, in which the `bot` is saved for later use, and a instance of `ChatBot` is saved and trained in english.

```Python
    @commands.command()
    async def say(self, *text):
        await self.bot.say(' '.join(text))
```

Create a command with a name of `say`.

Echos whatever the command executor says after the command.

```Python
    @commands.command()
    async def ping(self):
        await self.bot.say('Pong')
```

Creates a command with a name of `ping`, which simply has the bot say 'Pong' in response.

```Python
    @commands.command()
    async def decide(self, *options):
        if len(options) < 2:
            await self.bot.say('Not enough options to choose from')
        else:
            await self.bot.say(random.choice(options))
```

Creates a command with a name of `decide`, which can take a infinate amount of paramaters.

Outputs one of the given paramaters.

```Python
    @commands.command()
    async def translate(self, language, *text):
        translation = Translator(to_lang=language).translate(' '.join(text))

        await self.bot.say(translation)
```

Creates a command named `translate` which translate text from english to the two-character language code provided in the first argument, with the text-to-translate being all arguments after the first.

```Python
    @commands.command()
    async def talk(self, *message):
        reply = self.chatbot.get_response(" ".join(message))
        await self.bot.say(reply, tts=True)
```

Creates a command named `talk` which sends all following arguments to the ChatBot instance as a message, and relays the response of the ChatBot.

```Python
    @commands.command()
    async def quote(self, choice):
```

Create a command named `quote` which requires one argument.

This command will either respond with a random quote, or the quote of the day depending on the provided string in `choice`.

```Python
        if choice.upper() == 'QOTD':
            quote = wikiquote.quote_of_the_day()
            await self.bot.say("'{}' -- {}".format(quote[0], quote[1]))
```

Outputs the quote of the day if the choice equals `QOTD`, including the quote author.

```Python
        elif choice.upper() == 'R':
            while True:
```

Begining to output a random quote if the choice equals `R`.

The `while` loop is incase the found quote is blank or the randomly-chosen page has no quotes on it.

```Python
                pages = wikiquote.random_titles(max_titles=5)
                random_page = random.choice(pages)
                if random_page.isdigit():
                    continue
                random_quote = random.choice(wikiquote.quotes(random_page))
                await self.bot.say("'{}' -- {}"
                                   .format(random_quote,
                                           random_author))
                break
```

First gets five random pages and choses a page from one of these pages.

If the chosen page is a number, then the while loop continues.

Otherwise, a random quote is fetched from this page, and the bot outputs the quote and the author of the quote.

```Python
    @commands.command()
    async def time(self, timezone_code):
        local_time = datetime.now(get_localzone())
        converted_time = datetime.now(timezone(timezone_code.upper()))
        await self.bot.say("```Local time : {} \n\n   {}     : {}```"
                           .format(local_time, timezone_code, converted_time))
```

Creates a command named `time`, requireing one argument.

This command attempts to show the time in the given timezone code along side the localtime of the bot.

```Python
def setup(bot):
    bot.add_cog(Chat(bot))
```

Add the chat cog to the bot.