"""Chat cog.

Will contains many chat-related features.

"""
from discord.ext import commands
from chatterbot import ChatBot
from .utils import fileIO
import asyncio
import json
import time

def get_time_difference(time_one, time_two):
    """Get difference in days, hours, and minutes between two times."""
    diff = time.strftime("%d %H:%M",
                         time.gmtime(time_one - float(time_two)))
    diff = diff.replace(diff.split(" ")[0],
                        str(int(diff.split(" ")[0]) - 1))
    return diff


def UTC_string_to_string_time(UTC):
    """Return a formated time from a string UTC time."""
    return time.strftime("%m-%d-%Y %I:%M %p", time.gmtime(float(UTC)))


class Chat:
    """Chat cog."""

    def __init__(self, bot):
        """Initalization Function."""
        self.bot = bot
        asyncio.ensure_future(self.log_users())
#       Unsure if this is the best way to add an event.

    async def log_users(self):
        """Log all online users as online."""
        while True:
            await asyncio.sleep(10)
            try:
                data = fileIO.readFile("data/seen.json")
#               with open("data/seen.json",
#                         encoding="utf-8",
#                         mode="r") as seen:
#                   data = json.loads(seen.read())
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
#           with open("data/seen.json", encoding="utf-8", mode="w") as seen:
#               seen.write(json.dumps(data,
#                                     indent=4,
#                                     sort_keys=True,
#                                     separators=(',', ' : ')))


    @commands.command(hidden=True)
    async def say(self, *text):
        """Command that echos what you say.

        Keyword arguments:
        *text -- Text to echo
        """
        await self.bot.say(' '.join(text))

    @commands.command(pass_context=True, name="eval")
    async def _eval(self, ctx):
        eval(" ".join(ctx.message.content.split(" ")[1:]), {"self": self, "ctx": ctx})

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

    @commands.command(pass_context=True)
    async def seen(self, ctx, *target_users: str):
        """Return how long ago supplied target_user has been online.

        Keyword arguments:
        target_user -- Name of user to lookup.

        """
        for target_user in target_users:
            logged_users = fileIO.readFile("data/seen.json")
#           with open("data/seen.json", encoding="utf-8", mode="r") as seen:
#               logged_users = json.loads(seen.read())
            if "<@" in target_user:
                target_user = target_user.split("<@")[1].split(">")[0]
                if target_user in logged_users:
                    found_users = [logged_users[target_user]]
            else:
                found_users = [logged_users[user_id] for user_id in logged_users if logged_users[user_id]["name"].lower() == target_user.lower()]
            if found_users == []:
                await self.bot.say("{} could not be found..."
                                   .format(target_user))
                return

            for found_user in found_users:
                online_diff = get_time_difference(time.time(), found_user["last_online"])
                last_at_keyboard_diff = get_time_difference(time.time(), found_user["last_at_keyboard"])
                await self.bot.say("```\n"
                                   "|{}\n"
                                   "|             D  H M\n"
                                   "|Online:      {}\n"
                                   "|At Keyboard: {}"
                                   "```"
                                   .format(found_user["name"],
                                           online_diff,
                                           last_at_keyboard_diff))



def setup(bot):
    """Called when cog is loaded via load_extension()."""
    bot.add_cog(Chat(bot))
