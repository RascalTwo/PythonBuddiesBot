#Comic Scraper

##Overview

The purpose of the comic scraper cog is to scrape comic websites and show both the title and image of the comic to the user.

It can do this any way, although the general way is to scrape the comic title, and then scrape the URL to the comic image, and lastly to speak both of these into chat.

Currently, the Comic Scraper is ~~partly modularized. Each comic website to be scraped has it's own python file, with the name of the comic site as the filename.~~ a single file, as a method that did not include "indirection" created by the random and latest invokers.

##Commands

There are three commands native to the main comic scraper cog:

###Comic

This command is the main command that houses the random and latest command, and the group command for each comic module.

###Random

This command chooses a random comic website group command, and calls the random method within.

###Latest

Executes the latest command of the current comic. Subsequent execution calls the latest command from the next comic module.

Otherwords, it will fetch the latest comic for all loaded comic modules, and then show the latest comic for the first comic module once it reaches the last comic module.

##Comic Module Standards

> Are subject to change until this message is removed.

Add commands for a comic website in the middle of two comments, the first stating that code for the comic addition is begining, and another that declares the code for the comic addition is ending.

Methods that you think may be usable by other comic websites can be added near the bottom of the file, outside of the class.

If you find a method that you can actually use for the current comic you're scraping, you may move the method along side the other methods.

Prefix the commands for your comic addition with your decided name for the comic additions.

Add your `_random` and/or `_latest` command to the `latest_commands` and/or `random_commands` lists in the `__init__` method.

##Code Walkthough

*****

###Main Code Walkthrough

*****

```Python
import re
```

Import [regex](https://docs.python.org/3/library/re.html) module.

Used to replace HTML ASCII entities with their actual characters.

```Python
import random
```

Import [random](https://docs.python.org/3/library/random.html) module.

Used to choose both a random page of comics and a random comic from that page.

```Python
from .discord.ext import commands
```

Import the commands module from discord.

Used to register commands.

```Python
from .scraper_utils import GeneralScraper
```

Import a utility file that takes care of headers and making HTTP requests.

Used to fetch the pages of comic website which we scrape from.

***

```Python
class ComicScraper(GeneralScraper):
```

Create the class as a subclass of the GeneralScraper

```Python
    def __init__(self, bot):
```

Initalization method, requires the bot as an argument.

```Python
        super().__init__()
```

Calls the Initalization method of the class `ComicScraper` is a subclass of, which is `GeneralScraper`.


```Python
        self.bot = bot
```

`self.bot` is given the value of `bot`.

Used later to have the bot say things.


```Python
        self.latest_commands = []
        self.random_commands = []
```

Lists are created to hold the `latest` and `random` commands for each comic addition.

Used by the `comic_random` and `comic_latest` commands.


```Python
        self.current_comic = 0
```

Sets `self.current_comic` to 0

Used by `comic_latest`, allowing for the command to cycle through all comic additions in order.

*****

```Python
        self.latest_commands.append(self.commitstrip_latest)
        self.random_commands.append(self.commitstrip_random)
```

Add the `commitstrip_latest` command to `self.latest_commands` and `commitstrip_random` to `self.random_commands`

Allowing them to be executed by the `comic_latest` and `comic_random` commands.

```Python
        self.latest_commands.append(self.cubedrone_latest)
        self.random_commands.append(self.cubedrone_random)
```

Add the `cubedrone_latest` command to `self.latest_commands` and `cubedrone_random` to `self.random_commands`

Allowing them to be executed by the `comic_latest` and `comic_random` commands.

*****

```Python
    @commands.group(pass_context=True)
    async def comic(self, ctx):
```

Creates a group command with a name of `comic`, and pass context to the method.

The main comic command that contains `comic_random`, `comic_latest`, and all other comic addition group commands.

```Python
        if ctx.invoked_subcommand is None:
            await ctx.bot.pm_help(ctx)
```

Sends the user a help message if no subcommand is executed.

*****

```Python
    @comic.command(name="random", pass_context=True)
    async def comic_random(self, ctx):
```

Create a subcommand of `comic` with the name of `random`, and pass Context to the method.

```Python
        await random.choice(self.random_commands).invoke(ctx)
```

Execute a random command from `self.random_commands`.

*****

```Python
    @comic.command(name="latest", pass_context=True)
    async def comic_latest(self, ctx):
```

Create a subcommand of `comic` with the name of `latest`, and pass Context to the method.

```Python
        await self.latest_commands[self.current_comic].invoke(ctx)
```

Execute `self.current_comic`th command in `self.latest_commands`.

```Python
        self.current_comic = self.current_comic + 1 if self.current_comic != len(self.latest_commands)-1 else 0
```

Increment `self.current_comic` by one if there are `self.current_comic`+1 commands in `latest_commands`, else set it to 0.

*****

###CommitStrip Code Walkthrough

*****

```Python
    @comic.group(pass_context=True)
    async def commitstrip(self, ctx):
```

Creates a group command with a name of `comic`, and pass context to the method.

The main comic command that contains `comic_random`, `comic_latest`, and all other comic addition group commands.

```Python
        if ctx.invoked_subcommand is None:
            await self.bot.pm_help(ctx)
```

Sends the user a help message if no subcommand is executed.

```Python
    @commitstrip.command(name="random")
    async def commitstrip_random(self):
```

Create a subcommand of `commitstrip` with a name of `random`.

Command to have the bot output a random comic title and url to said random comic image.

```Python
        message = await ctx.bot.say("Loading...")
```

Sends a loading message instantly so the user knows the command was sent successfully. Will be edited with the results once fetching and scraping of the comic is complete. This is not necessary

```Python
        index_html = (await self.fetch_page("http://www.commitstrip.com/")).decode("utf-8")
```

Calls the internal `self.fetch_page` method, passing the URL to the webpage where the number of pages of comics can be scraped from. Since the `fetch_page` method returns the data in `bytes`, it needs to be decoded into `utf-8`.

```Python
        last_page_number = int(index_html.split('<a class="last" href="')[1].split('"')[0].split("/")[5].split("/")[0])
```

Gets the number of the last page.

First gets the URL within the `a` element with a class of `last`. Then get the text after the 5th forward slash, split away the trailing forward slash, and lastly convert it into an `int`.

```Python
        random_page_url = "http://www.commitstrip.com/en/page/{}".format(random.randint(1, last_page_number))
```

The URL of the random page to be fetched, can be from 1 to `last_page_number`.

```Python
        random_page = (await self.fetch_page(random_page_url)).decode("utf-8")
```

Again execute `fetch_page`, this time getting a the above `random_page_url`.

```Python
        comic_list_html = [comic_raw.split("</div>")[0] for comic_raw in random_page.split('<div class="excerpt">')]
```

A one-line for loop that gets the raw HTML for each comic. Is the equivalent to this:

***
EXAMPLE CODE - NOT ACTUAL CODE
```Python
comic_list_html = []
for comic_raw in random_page.split('<div class="excerpt">'):
    comic_list_html.append(comic_raw.split("</div>")[0])
```
EXAMPLE CODE - NOT ACTUAL CODE
***

```Python
        comic_list_html.pop(0)
```

Remove the 0th (read first) element from `comic_list_html`, as the 0th (read first) is all the HTML code before the first actual comic.

```Python
        comic_url = random.choice(comic_list_html).split('<a href="')[1].split('"')[0]
```

Strip the URL of a random comic html.

```Python
        comic = (await self.commitstrip_comic_from_url(comic_url))
```

Executes the internal method `commitstrip_comic_from_utl`, passing the URL to the comic we have randomly chosen to show to the user.

```Python
        await self.bot.edit_message(message, "**Title**: `{}`\n"
                                             "**Image**: {}".format(comic[0],
                                                                    comic[1]))
```

Edit the previously sent `Loading...` message with both the Title and the URL to the comic.

> The spacing is like it is because Pylint wants it this way.

***

```Python
    @commitstrip.command(name="latest")
    async def commitstrip_latest(self):
```

Create a subcommand of `commitstrip` with a name of `latest`.

Command to have the bot output the latest comic of this comic addition.

```Python
        message = await self.bot.say("Loading...")
```

Sends a loading message instantly so the user knows the command was sent successfully. Will be edited with the results once fetching and scraping of the comic is complete. This is not necessary

```Python
        index_html = (await self.fetch_page("http://www.commitstrip.com/")).decode("utf-8")
```

Calls the internal `self.fetch_page` method, passing the URL to the webpage where the number of pages of comics can be scraped from. Since the `fetch_page` method returns the data in `bytes`, it needs to be decoded into `utf-8`.

```Python
        url_http = index_html.split('<div class="excerpt">')[1].split('<a href="')[1].split('"')[0]
```

Scrape the URL of the first comic.

```Python
        comic = (await self.commitstrip_comic_from_url(self, url_http))
```

Executes the internal method `commitstrip_comic_from_url`, passing the URL to the comic we have randomly chosen to show to the user.

```Python
        await self.bot.edit_message(message, "**Title**: `{}`\n"
                                            "**Image**: {}".format(comic[0],
                                                                comic[1]))
```

Edit the previously sent `Loading...` message with both the Title and the URL to the comic.

***

```Python
    async def commitstrip_comic_from_url(self, comic_url):
```

Creating the asynchronous `commitstrip_comic_from_url` method, which will return the comic title and the URL to the comic image while being passed the Context and the URL to the comic.

```Python
        comic_html = (await self.fetch_page(comic_url)).decode("utf-8")
```

Calls the internal `self.fetch_page` method, passing the URL to the webpage where the number of pages of comics can be scraped from. Since the `fetch_page` method returns the data in `bytes`, it needs to be decoded into `utf-8`.

```Python
        comic_image = comic_html.split('<div class="entry-content">')[1].split("<img ")[1].split('src="')[1].split('"')[0]
```

Scrapes the comic image URL from the div with a clas of `entry-content`, of which there is only one on the webpage.

It is not scraped like shown below due to the fact that sometimes there is an attribute between the opening `img` tag and the `src` attribute.

***
EXAMPLE CODE - NOT ACTUAL CODE
```Python
        comic_image = comic_html.split('<div class="entry-content">')[1].split('<img src="')[1].split('"')[0]
```
EXAMPLE CODE - NOT ACTUAL CODE
***

```Python
        comic_title = comic_html.split('<h1 class="entry-title">')[1].split("</h1>")[0]
```

Scrape the comic title from within the `h1` element with a class of `entry-title`, of which there are only one on the webpage.

```Python
        return [parse_html_entities(comic_title), comic_image]
```

Return a list in which the 0th (read first) element is the title of the comic, and the 1st (read second) is the URL to the comic image.

The public method `parse_html_entities` is performed on `comic_title` before it is returned due to the fact that it sometimes contains HTML ASCII entities within it.

*****

###CubeDrone Code Walkthrough

*****

Coming Soon, it's nearly the same as above though. Only real changes are scraping.

*****

###Main Code Walkthrough

*****

```Python
def parse_html_entities(string):
```

Creating the `parse_html_entities` method, which will replace HTML ASCII entities - &#1234; - with the actual characters they represent.

```Python
    for hit in re.findall("&#\d+;", string):
```

For every match found by the regex expression supplied

Regex expression explanation:

`&#\\d+;`

```
&# matches the characters &# literally
\\d match a digit [0-9] - there are two backslashes to please Pylint.
+ Between one and unlimited times of the previous match, as many times as possible
; matches the character ; literally
```

```Python
        try:
            string = string.replace(hit, chr(int(hit[2:-1])))
        except ValueError:
            pass
```

Attempt to replace the found match with the character that matches the code within the match - the numbers.

```Python
    return string
```

Return the parsed string, free of HTML ASCII entities.

***

```Python
def setup(bot):
    bot.add_cog(ComicScraper(bot))
```

Add the `ComicScraper` cog to the bot.