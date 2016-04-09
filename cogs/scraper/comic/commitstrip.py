"""Commitstrip comic scraper.

Get the latest or a random comic from http://www.commitstrip.com/

"""

from .comic_scraper import ComicScraper
import random
import re

class CommitStrip(object):
    """Holds the commands and methods for returning CommitStrip comics."""

    @ComicScraper.comic.group(pass_context=True)
    async def commitstrip(ctx):
        """Main CommitStrip command."""
        if ctx.invoked_subcommand is None:
            await self.bot.pm_help(ctx)

    @commitstrip.command(name="random", pass_context=True)
    async def commitstrip_random(ctx):
        """Return a random CommitStrip comic."""
        # Get the last page number
        message = await ctx.bot.say("Loading...")
        index_html = (await ctx.bot.cogs["ComicScraper"].fetch_page("http://www.commitstrip.com/")).decode("utf-8")
        last_page_number = int(index_html.split('<a class="last" href="')[1].split('"')[0].split("/")[5].split("/")[0])

        # Get the HTML of a random page between 1 and last page number
        random_page = (await ctx.bot.cogs["ComicScraper"].fetch_page("http://www.commitstrip.com/en/page/{}".format(random.randint(1, last_page_number)))).decode("utf-8")
        comic_list_html = [comic_raw.split("</div>")[0] for comic_raw in random_page.split('<div class="excerpt">')]

        # Get rid of all non-comic code before first '<div class="excerpt">'
        comic_list_html.pop(0)

        # Get the title and image of random comic.
        comic = (await CommitStrip.commitstrip_comic_from_url(ctx, random.choice(comic_list_html).split('<a href="')[1].split('"')[0]))
        await ctx.bot.edit_message(message, "**Title**: `{}`\n"
                                            "**Image**: {}"
                                            .format(comic[0], comic[1]))

    @commitstrip.command(name="latest", pass_context=True)
    async def commitstrip_latest(ctx):
        """Return the latest CommitStrip comic."""
        message = await ctx.bot.say("Loading...")
        index_html = (await ctx.bot.cogs["ComicScraper"].fetch_page("http://www.commitstrip.com/")).decode("utf-8")
        url_http = index_html.split('<div class="excerpt">')[1].split('<a href="')[1].split('"')[0]
        comic = (await CommitStrip.commitstrip_comic_from_url(ctx, url_http))
        await ctx.bot.edit_message(message, "**Title**: `{}`\n"
                                            "**Image**: {}"
                                            .format(comic[0], comic[1]))

    @staticmethod
    async def commitstrip_comic_from_url(ctx, comic_url):
        """Return comic title and comic image url from comic page url.

        Keyword Arguments:
        ctx -- Context object
        comic_url -- URL of comic page.

        Returns:
        list -- 0 -- str -- Title of comic.
                1 -- str -- URL of the comic image.

        """
        comic_html = (await ctx.bot.cogs["ComicScraper"].fetch_page(comic_url)).decode("utf-8")
        # 'src' is not always the first attribute after the opening img tag.
        comic_image = comic_html.split('<div class="entry-content">')[1].split("<img ")[1].split('src="')[1].split('"')[0]
        comic_title = comic_html.split('<h1 class="entry-title">')[1].split("</h1>")[0]
        return [CommitStrip.parse_html_entities(comic_title), comic_image]

    @staticmethod
    def parse_html_entities(string):
        """Replace ASCII character codes with the actual characters.

        Keyword Arguments:
        string -- String with ASCII codes within it.

        Returns:
        str -- 'string' with ASCII codes replaced with characters.

        Note: May be moved into a utility file if there is another
        time it is needed. Maybe into the GeneralScraper class.

        """
        for hit in re.findall("&#\d+;", string):
            try:
                string = string.replace(hit, chr(int(hit[2:-1])))
            except ValueError:
                pass
        return string


def setup(bot):
    """Added to prevent cog loading to throw an error.

    Improvements to cog loading and usage of __init__.py
    files will allow this to be removed in the future.

    """
    pass
