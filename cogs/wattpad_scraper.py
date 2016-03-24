"""Wattpad scraper cog.

Many features to scrap from wattpad.

"""
from discord.ext import commands
from .utils import wattpadscraper


class WattpadScraper:
    """Wattpad scraper cog."""

    def __init__(self, bot):
        """Initalization function."""
        self.bot = bot

    @commands.group(name='wattpad', pass_context=True)
    async def _wattpad(self, ctx):
        """Useful commands for getting stories from Wattpad."""
        if ctx.invoked_subcommand is None:
            await self.bot.pm_help(ctx)

    @_wattpad.command()
    async def latest(self):
        """Get the latest story posted to Wattpad."""
        result = await wattpadscraper.get_latest_story(self.bot.session)
        await self.bot.say(result)


def setup(bot):
    """Called when cog is loaded via load_extension()."""
    bot.add_cog(WattpadScraper(bot))
