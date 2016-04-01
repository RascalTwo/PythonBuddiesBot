"""Test cog."""
from discord.ext import commands


class Test:
    """Test cog."""

    def __init__(self, bot):
        """Initalization function."""
        self.bot = bot

    async def receive_message(self, message):
        """Called whenever any player sends a message."""
        if message.author.id == self.bot.user.id:
            return
        if "r/" in message.content or "u/" in message.content:
            replacies = []
            new_content = ""
            for part in message.content.split(" "):
                if "u/" in part or "r/" in part:
                    replacies.append(part)
            for replacie in replacies:
                thing = replacie if len(replacie.split("/")) == 3 else "/{}".format(replacie)
                new_content += " " + replacie.replace(replacie, "https://reddit.com{}".format(thing))
            await self.bot.send_message(message.channel, new_content)


def setup(bot):
    """Called when cog is loaded via load_extension()."""
    test = Test(bot)
    bot.add_listener(test.receive_message, "on_message")
    bot.add_cog(test)
