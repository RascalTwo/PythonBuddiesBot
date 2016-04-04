"""Chat cog.

Will contains many chat-related features.

"""
from discord.ext import commands
from chatterbot import ChatBot
from .utils import fileIO
import asyncio
import json
import time


class Chat:
    """Chat cog."""

    def __init__(self, bot):
        """Initalization Function."""
        self.bot = bot
        asyncio.ensure_future(self.log_users())
#       Unsure if this is the best way to add a recurring event.

    async def log_users(self):
        """Log all online users as online."""
        while True:
            await asyncio.sleep(60)
            try:
                data = fileIO.readFile("data/seen.json")
            except Exception as e:
                data = {}
            for member in self.bot.get_all_members():
                if str(member.status) == "offline":
                    continue
                if member.id not in data:
                    data[member.id] = {
                        "name": member.name,
                        "last_online": time.time()
                    }
                else:
                    data[member.id]["name"] = member.name
                    data[member.id]["last_online"] = time.time()
                if str(member.status) == "idle":
                    continue
                data[member.id]["last_at_keyboard"] = time.time()
            fileIO.writeFile("data/seen.json", data)

    @commands.command(hidden=True)
    async def say(self, *text):
        """Command that echos what you say.

        Keyword arguments:
        *text -- Text to echo
        """
        await self.bot.say(' '.join(text))

    @commands.command(pass_context=True)
    async def talk(self, ctx):
        """Command that implements the talk to the bot function.

        It uses ChatterBot, is a machine-learning based
        conversational dialog engine build in Python which makes
        it possible to generate responses based on collections of
        known conversations

        **Dependencies**: pip install chatterbot

        **Keyword Arguments**:
        chatbot -- stores chatbot object
        ctx     -- Context reference to get message
        tts     -- Set to true for text to speed implementation

        """
        chatbot = ChatBot("Ron Obvious")
        chatbot.train("chatterbot.corpus.english")
        msg = ctx.message.content
        print(msg)
        if msg.startswith('$talk'):
            msg = msg[6:]
            print(msg)
            reply = chatbot.get_response(msg)

        await self.bot.send_message(ctx.message.channel, reply, tts=True)

    @commands.command()
    async def seen(self, *target_users: str):
        """Return how long ago supplied user mentions or names have been online.

        Keyword arguments:
        usernames -- Names of user to lookup.

        """
        logged_users = fileIO.readFile("data/seen.json")
        for target_user in target_users:
            if "<@" in target_user:
                target_user = target_user.split("<@")[1].split(">")[0]
                if target_user in logged_users:
                    found_users = [logged_users[target_user]]
            else:
                found_users = [logged_users[user_id]
                               for user_id in logged_users
                               if logged_users[user_id]["name"].lower() == target_user.lower()]
            if found_users == []:
                await self.bot.say("{} could not be found..."
                                   .format(target_user))
                return

            for found_user in found_users:
                await self.bot.say("```\n"
                                   "┌───────────────────────┐\n"
                                   "├{}{}│\n"
                                   "│             D  H  M  S│\n"
                                   "├Online───────{}│\n"
                                   "├At Keyboard──{}│\n"
                                   "└───────────────────────┘\n"
                                   "```"
                                   .format(found_user["name"],
                                           " " * (23 - len(found_user["name"])),
                                           self.get_since(found_user["last_online"]),
                                           self.get_since(found_user["last_at_keyboard"])))

    def get_since(self, since_when):
        """Get time since 'since_when' in days, hours, and minutes.

        Keyword Arguments:
        since_when -- Time to get amount of days, hours, and
                      minutes it has been since.

        Returns:
        str -- String representation of how many
               days, hours, and minutes it's been since 'since_when'.
               Format  -  D  H:M
               Example - '5 06:24'

        """
        diff = time.strftime("%j %H:%M:%S",
                             time.gmtime(time.time() - float(since_when)))
        return diff.replace(diff.split(" ")[0],
                            str(int(diff.split(" ")[0]) - 1))


def setup(bot):
    """Called when cog is loaded via load_extension()."""
    bot.add_cog(Chat(bot))
