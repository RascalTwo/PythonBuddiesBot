from discord.ext import commands


# Chat cog
class Chat:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def say(self, *text):     # !say text
        """Command that echos what you say.

        Keyword arguments:
        *text -- Text to echo
        """
        await self.bot.say(' '.join(text))


def setup(bot):
    bot.add_cog(Chat(bot))
