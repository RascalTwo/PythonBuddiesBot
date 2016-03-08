from discord.ext import commands

from .utils import checks, scraper

class RedditScraper:

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(name='reddit', pass_context=True)
    @checks.is_owner()
    async def _reddit(self, ctx):
        """Useful commands for getting information from reddit."""
        if ctx.invoked_subcommand is None:
            await self.bot.pm_help(ctx)

    @_reddit.command(pass_context=True, name='get')
    async def get(self, ctx: commands.Context, subreddit, posts=5, category='hot'):
        """Base command for returning data from a subreddit.

        Keyword arguments:
        posts -- Number of posts to return (default 5)
        category -- Category to look at [hot, new, rising, controversial, top] (default hot)
        """
        if posts > 25:
            await self.bot.say('Number of posts must be no greater than 25.')
            return
        if subreddit.strip():
            if category in scraper.categories:
                result = await scraper.get_subreddit_top(self.bot.session, subreddit, posts, category)
                await self.bot.say('\n\n'.join(result))
            else:
                await self.bot.say('Category must be valid: ' + ', '.join(scraper.categories))
        else:
            await self.bot.pm_help(ctx)


def setup(bot):
    bot.add_cog(RedditScraper(bot))
