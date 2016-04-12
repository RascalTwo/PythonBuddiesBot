#Comic Scraper

##Overview

The purpose of the comic scraper cog is to scrape comic websites and show both the title and image of the comic to the user.

It can do this any way, although the general way is to scrape the comic title, and then scrape the URL to the comic image, and lastly to speak both of these into chat.

Currently, the Comic Scraper is partly modularized. Each comic website to be scraped has it's own python file, with the name of the comic site as the filename.

It is only partly modularized due to the fact that some not-obvious (read patchy) methods are being used to link the comic module subcommand to the main comic command.

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

The python file a comic module is contained within should either be named - preferably - the name of the comic series, or if not possible, the name of the website the comic series is on - without any HTTP prefixes or suffixes of course. Just make sure it's unique.

> From this point forward, the name you choose for the file name shall be refered to as the `comic module name`.

***

In order for the comic module subcommand to be attached to the comic scraper, ComicScraper must be imported into the comic module, like so:

```Python
from .comic_scraper import ComicScraper
```

***

Since these methods are not within a class them shall have the `self` argument added to them.

When linking your comic module command to the main comic command, you shall link it as such:

```Python
@ComicScraper.comic.group(pass_context=True)
async def `comic module name`(ctx):
```

That introduces another difference between normal commands and these: you will - almost always - want to set `pass_context` to `True`, as this is the only thing you're going to access bot commands with - since there is no `self` argument.

***

A setup method needs to be included at the end of the file. Nothing needs to be done in this method, so simply placing `pass` within it will be acceptable. Also name the argument a simple underscore - `_` - so pylint will not throw a error.

This is what makes the modularization only partial. When it is fully modularized, there will be no need to trick the bot into reading the file, which attaches the commands to the main comic command.

##Code Walkthough
```Python
import random
```

Required to choose both a random page of comics and a random comic from that page.

```Python
import re
```

Required to replace HTML ASCII entities with their actual characters.

```Python
from .comic_scraper import ComicScraper
```
As disucced above, needed for every comic module

***

```Python
@ComicScraper.comic.group(pass_context=True)
async def commitstrip(ctx):
```

Creating the `commitstrip` group command as a subcommand of the main `comic` command from `ComicScraper`.

```Python
    if ctx.invoked_subcommand is None:
        await ctx.bot.pm_help(ctx)
```

Send the help message for the command is no subcommand is executed.

***

```Python
@commitstrip.command(name="random", pass_context=True)
async def commitstrip_random(ctx):
```

Creating the `random` subcommand for the `commitstrip` command.

```Python
    message = await ctx.bot.say("Loading...")
```

Sends a loading message instantly so the user knows the command was sent successfully. Will be edited with the results once fetching and scraping of the comic is complete. This is not necessary

```Python
    index_html = (await ctx.bot.cogs["ComicScraper"].fetch_page("http://www.commitstrip.com/")).decode("utf-8")
```

Calls the `fetch_page` method of the `ComicScraper` cog, passing the URL to the webpage where the number of pages of comics can be scraped from. Since the `fetch_page` method returns the data in `bytes`(?), it needs to be decoded into `utf-8`.

```Python
    last_page_number = int(index_html.split('<a class="last" href="')[1].split('"')[0].split("/")[5].split("/")[0])
```

Gets the number of the last page.

First gets the URL within the `a` element with a class of `last`. Then get the text after the 5th forward slash, split away the trailing forward slash, and lastly convert it into a `int`.

```Python
    random_page_url = "http://www.commitstrip.com/en/page/{}".format(random.randint(1, last_page_number))
```

The URL of the random page to be fetched, can be from 1 to `last_page_number`.

```Python
    random_page = (await ctx.bot.cogs["ComicScraper"].fetch_page(random_page_url)).decode("utf-8")
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

***

```Python
    comic_list_html.pop(0)
```

Remove the 0th (read first) element from `comic_list_html`, as the 0th (read first) is all the HTML code before the first actual comic.

```Python
    comic = (await CommitStrip.commitstrip_comic_from_url(ctx, random.choice(comic_list_html).split('<a href="')[1].split('"')[0]))
```

Executes the internal method `commitstrip_comic_from_utl`, passing the current Context object - ctx - and the URL to the comic we have randomly chosen to show to the user.

```Python
    await ctx.bot.edit_message(message, "**Title**: `{}`\n"
                                        "**Image**: {}".format(comic[0],
                                                               comic[1]))
```

Edit the previously sent `Loading...` message with both the Title and the URL to the comic.

> The spacing is like it is because Pylint wants it this way.

***

```Python
@commitstrip.command(name="latest", pass_context=True)
async def commitstrip_latest(ctx):
```

Creating the `latest` subcommand for the `commitstrip` command.

```Python
    message = await ctx.bot.say("Loading...")
```

Sends a loading message instantly so the user knows the command was sent successfully. Will be edited with the results once fetching and scraping of the comic is complete. This is not necessary

```Python
    index_html = (await ctx.bot.cogs["ComicScraper"].fetch_page("http://www.commitstrip.com/")).decode("utf-8")
```

Calls the `fetch_page` method of the `ComicScraper` cog, passing the URL to the webpage where the number of pages of comics can be scraped from. Since the `fetch_page` method returns the data in `bytes`(?), it needs to be decoded into `utf-8`.

```Python
    url_http = index_html.split('<div class="excerpt">')[1].split('<a href="')[1].split('"')[0]
```

Scrape the URL of the first comic.

```Python
    comic = (await CommitStrip.commitstrip_comic_from_url(ctx, url_http))
```

Executes the internal method `commitstrip_comic_from_utl`, passing the current Context object - ctx - and the URL to the comic we have randomly chosen to show to the user.

```Python
    await ctx.bot.edit_message(message, "**Title**: `{}`\n"
                                        "**Image**: {}".format(comic[0],
                                                               comic[1]))
```

Edit the previously sent `Loading...` message with both the Title and the URL to the comic.

***

```Python
async def commitstrip_comic_from_url(ctx, comic_url):
```

Creating the asynchronous `commitstrip_comic_from_url` method, which will return the comic title and the URL to the comic image while being passed the Context and the URL to the comic.

```Python
    comic_html = (await ctx.bot.cogs["ComicScraper"].fetch_page(comic_url)).decode("utf-8")
```

Calls the `fetch_page` method of the `ComicScraper` cog, passing the alredy-supplied URL `comic_url`. Since the `fetch_page` method returns the data in `bytes`(?), it needs to be decoded into `utf-8`.

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

***

```Python
    comic_title = comic_html.split('<h1 class="entry-title">')[1].split("</h1>")[0]
```

Scrape the comic title from within the `h1` element with a class of `entry-title`, of which there are only one on the webpage.

```Python
    return [CommitStrip.parse_html_entities(comic_title), comic_image]
```

Return a list in which the 0th (read first) element is the title of the comic, and the 1st (read second) is the URL to the comic image.

The internal method `parse_html_entities` is performed on `comic_title` before it is returned due to the fact that it sometimes contains HTML ASCII entities within it.

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
def setup(_):
    pass
```

A two purpose method. The first of which is to not have the bot throw an error when attempting to load the file, and second of which is to allow the file to be imported, making it usable by `ComicScraper`.
