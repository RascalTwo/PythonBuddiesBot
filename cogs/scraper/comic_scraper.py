"""Comic scraper cog.

Contains comic, comic random, and comic latest commands - the latter
two choose a random command from sub-group-commands of comic to execute.

"""
import random
from discord.ext import commands
from .scraper_utils import GeneralScraper

class ComicScraper(GeneralScraper):
    """Main base comic cog.

    Extends GeneralScraper.
    Contains the comic, comic latest, and comic random commands.

    """

    def __init__(self, bot):
        """Initalization method."""
        super().__init__()
        self.bot = bot
        self.latest_commands = []
        self.random_commands = []
        self.current_comic = 0

    @commands.group(pass_context=True)
    async def comic(self, ctx):
        """Main comic command."""
        if ctx.invoked_subcommand is None:
            await ctx.bot.pm_help(ctx)

    @comic.command(name="random", pass_context=True)
    async def comic_random(self, ctx):
        """Return random comic from a random comic website."""
        await random.choice(self.random_commands).invoke(ctx)

    @comic.command(name="latest", pass_context=True)
    async def comic_latest(self, ctx):
        """Return the latest comic from the next comic website."""
        await self.latest_commands[self.current_comic].invoke(ctx)
        self.current_comic = self.current_comic + 1 if self.current_comic != len(self.latest_commands)-1 else 0


def setup(bot):
    """Called when cog is loaded via load_extension()."""
    bot.add_cog(ComicScraper(bot))
