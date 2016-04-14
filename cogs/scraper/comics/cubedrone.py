"""CubeDrone comic scraper.

Get the latest or a random comic from http://www.cube-drone.com/

"""
import random
import re
from ..comic_scraper import ComicScraper


@ComicScraper.comic.group(pass_context=True)  # pylint: disable=no-member
async def cubedrone(ctx):
    """Main CubeDrone command."""
    if ctx.invoked_subcommand is None:
        await ctx.bot.pm_help(ctx)


@cubedrone.command(name="random", pass_context=True)
async def cubedrone_random(ctx):
    """Return a random CubeDrone comic."""
    # Get the last page number
    message = await ctx.bot.say("Loading...")
    index_html = (await ctx.bot.cogs["ComicScraper"].fetch_page("https://cube-drone.com/")).decode("utf-8")
    total_comics = int(index_html.split("<div class='order bg-primary'>")[1].split("</div>")[0])
    comic_url = "https://cube-drone.com/comics/n/{}".format(random.randint(1, total_comics))
    comic = (await cubedrone_comic_from_url(ctx, comic_url))
    await ctx.bot.edit_message(message, "**Title**: `{}`\n"
                                        "**Image**: {}".format(comic[0],
                                                               comic[1]))


@cubedrone.command(name="latest", pass_context=True)
async def cubedrone_latest(ctx):
    """Return the latest CubeDrone comic."""
    message = await ctx.bot.say("Loading...")
    comic = (await cubedrone_comic_from_url(ctx, "https://cube-drone.com/"))
    await ctx.bot.edit_message(message, "**Title**: `{}`\n"
                                        "**Image**: {}".format(comic[0],
                                                               comic[1]))


async def cubedrone_comic_from_url(ctx, comic_url):
    """Return comic title and comic image url from comic page url.

    Keyword Arguments:
    ctx -- Context object
    comic_url -- URL of comic page.

    Returns:
    list -- 0 -- str -- Title of comic.
            1 -- str -- URL of the comic image.

    """
    comic_html = (await ctx.bot.cogs["ComicScraper"].fetch_page(comic_url)).decode("utf-8")
    comic_image = comic_html.split("<img class='comic img-responsive' src='")[1].split("'")[0]
    comic_title = comic_html.split("<h2 class='comic_title'>")[1].split("<small>")[0]
    return [parse_html_entities(comic_title), comic_image]


def parse_html_entities(string):
    """Replace ASCII character codes with the actual characters.

    Keyword Arguments:
    string -- String with ASCII codes within it.

    Returns:
    str -- 'string' with ASCII codes replaced with characters.

    Note: May be moved into a utility file if there is another
    time it is needed. Maybe into the GeneralScraper class.

    """
    for hit in re.findall("&#\\d+;", string):
        try:
            string = string.replace(hit, chr(int(hit[2:-1])))
        except ValueError:
            pass
    return string

def setup(bot):
    """Called when cog is loaded via load_extension()."""
    bot.cogs["ComicScraper"].random_commands.append(cubedrone_random)
    bot.cogs["ComicScraper"].latest_commands.append(cubedrone_latest)
