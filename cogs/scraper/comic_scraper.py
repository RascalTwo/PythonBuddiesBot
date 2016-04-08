from datetime import datetime
from discord.ext import commands
from .scraper_utils import GeneralScraper
import random

@commands.group(pass_context=True)
async def comic(ctx):
    """Main comic command."""
    if ctx.invoked_subcommand is None:
        await self.bot.pm_help(ctx)

class ComicScraper(GeneralScraper):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.current_comic = 0

    @comic.command(name="random", pass_context=True)
    async def comic_random(self, ctx):
        """Random random function executor."""
        random_methods = [getattr(self, method_name) for method_name in dir(self) if "_random" in method_name and "comic_random" != method_name]
        await random_methods[random.randint(0, len(random_methods)-1)].invoke(ctx)

    @comic.command(name="latest", pass_context=True)
    async def comic_latest(self, ctx):
        """Random random function executor."""
        latest_methods = [getattr(self, method_name) for method_name in dir(self) if "_latest" in method_name and "comic_latest" != method_name]
        await latest_methods[self.current_comic].invoke(ctx)
        self.current_comic = self.current_comic + 1 if self.current_comic != len(latest_methods)-1 else 0

# Begin CommitStrip

class CommitStrip(object):

    @comic.group(pass_context=True)
    async def commitstrip(self, ctx):
        """Main CommitStrip command."""
        if ctx.invoked_subcommand is None:
            await self.bot.pm_help(ctx)

    @commitstrip.command(name="random")
    async def commitstrip_random(self):
        """ Random commitstrip comic"""

        # Get the last page number
        # Get the HTML of a random page between 1 and last page number
        # Pick a random comic from the picked page
        # Get the title and image of comic.
        index_html = (await self.fetch_page("http://www.commitstrip.com/")).decode("utf-8")
        last_page_number = int(index_html.split('<a class="last" href="')[1].split('"')[0].split("/")[5].split("/")[0])

        random_page = (await self.fetch_page("http://www.commitstrip.com/en/page/{}".format(random.randint(1, last_page_number)))).decode("utf-8")
        comic_list_html = [comic_raw.split("</div>")[0] for comic_raw in random_page.split('<div class="excerpt">')]
        comic_list_html.pop(0)

        comic = (await self.commitstrip_comic_from_link(comic_list_html[random.randint(0, len(comic_list_html)-1)].split('<a href="')[1].split('"')[0]))
        await self.bot.say("**Title**: `{}`\n"
                           "**Image**: {}"
                           .format(comic[0], comic[1]))

    @commitstrip.command(name="latest")
    async def commitstrip_latest(self):
        """ Random commitstrip comic"""
        index_html = (await self.fetch_page("http://www.commitstrip.com/")).decode("utf-8")
        link_http = index_html.split('<div class="excerpt">')[1].split('<a href="')[1].split('"')[0]
        comic = (await self.commitstrip_comic_from_link(link_http))
        await self.bot.say("**Title**: `{}`\n"
                           "**Image**: {}"
                           .format(comic[0], comic[1]))

    async def commitstrip_comic_from_link(self, comic_link):
        comic_html = (await self.fetch_page(comic_link)).decode("utf-8")
        comic_image = comic_html.split('<div class="entry-content">')[1].split("<img ")[1].split('src="')[1].split('"')[0]
        comic_title = comic_html.split('<h1 class="entry-title">')[1].split("</h1>")[0]
        return [comic_title, comic_image]

# End CommitStrip


def setup(bot):
    bot.add_cog(ComicScraper(bot))
