from discord.ext import commands

from .utils import checks, wattpadscraper

class WattpadScraper:
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.group(name ='wattpad',pass_context = True)
    @checks.is_owner()
    async def _wattpad(self,ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.pm_help(ctx)

    @_wattpad.command(pass_context=True,name = 'fetch')
    async def fetch(self, ctx: commands.Context):
        result = await wattpadscraper.get_random_story_info(self.bot.session)
        await self.bot.say(result)

def setup(bot):
    bot.add_cog(WattpadScraper(bot))
