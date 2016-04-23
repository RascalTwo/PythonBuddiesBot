"""Chat cog.

Contains many all chat-related commands.

"""
import random
from datetime import datetime
from pytz import timezone
from tzlocal import get_localzone
from discord.ext import commands
from chatterbot import ChatBot
from translate import Translator
from .utils import fileIO
import asyncio
import json
import time
from .scraper.scraper_utils import GeneralScraper
import re
from .queue import Loop


class Chat(GeneralScraper):
    """Card cog."""

    def __init__(self, bot):
        """Initalization function."""
        super().__init__()
        self.bot = bot
        self.chatbot = ChatBot("Ron Obvious")
        self.chatbot.train("chatterbot.corpus.english")
        Loop(self.log_users, 60)

    def log_users(self):
        """Log all online users as online."""
        while True:
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
            time.sleep(60)

    @commands.command()
    @asyncio.coroutine
    def say(self, *text):
        """Echos what you say.

        Keyword arguments:
        *text -- Text to echo

        """
        yield from self.bot.say(' '.join(text))

    @commands.command()
    @asyncio.coroutine
    def ping(self):
        """Says 'Pong'.

        Keyword arguments:
        None

        """
        yield from self.bot.say('Pong')

    @commands.command()
    @asyncio.coroutine
    def decide(self, *options):
        """Decides between multiple options

        **Use double quotes for each option**

        Keyword arguments:
        options

        """
        if len(options) < 2:
            yield from self.bot.say('Not enough options to choose from')
        else:
            yield from self.bot.say(random.choice(options))

    @commands.command()
    @asyncio.coroutine
    def translate(self, language, *text):
        """Translates text from English to specified language

        **Use double quotes for each option**

        **Dependencies**: pip install translate
                          (https://github.com/terryyin/google-translate-python)

        Keyword arguments:
        language -- Two-letter code for the languate to translate to
        text -- Text to translate.

        """
        text_to_string = ''.join(text)
        translator = Translator(to_lang=language)
        translation = translator.translate(text_to_string)

        yield from self.bot.say(translation)

    @commands.command()
    @asyncio.coroutine
    def talk(self, *message):
        """Speak to ChatterBot.

        It uses ChatterBot, is a machine-learning based
        conversational dialog engine build in Python which makes
        it possible to generate responses based on collections of
        known conversations

        **Dependencies**: pip install chatterbot

        Keyword arguments:
        message -- Message to send to the chatbot.

        """
        reply = self.chatbot.get_response(" ".join(message))
        yield from self.bot.say(reply, tts=True)

    @commands.command()
    @asyncio.coroutine
    def quote(self, choice):
        """Generating a random quote or get the quote of the day.

        **Dependencies**: pip install wikiquote

        Keyword arguments:
        choice -- either 'QOTD' (Quote of the day) or 'R' (Random)

        """

        if choice.upper() == 'QOTD':
            html = yield from self.fetch_json("https://en.wikiquote.org/w/api.php?format=json&action=parse&prop=text&page=Main%20Page")
            html = html["parse"]["text"]["*"]
            html = html.split("Quote of the day")[1].split("<table")[3].split("<td>")[1].split("</table>")[0]
            qotd = striphtml(html)
            yield from self.bot.say("{}".format(qotd))
#        elif choice.upper() == 'R':
#            pass
         #   while True:
            #    authors = wikiquote.random_titles(max_titles=5)
            #    random_author = random.choice(authors)
            #    if random_author.isdigit():
            ###        continue
              #  random_quote = random.choice(wikiquote.quotes(random_author))
              ##  yield from self.bot.say("'{}' -- {}"
               #                    .format(random_quote,
               #                            random_author))
               # break

    @commands.command()
    @asyncio.coroutine
    def time(self, timezone_code):
        """Return current time and time in the timezone listed.

        **Dependencies**: pip install pytz tzlocal

        Keyword arguments:
        timezone_code  -- Code for timezone
        """
        local_time = datetime.now(get_localzone())
        converted_time = datetime.now(timezone(timezone_code.upper()))
        yield from self.bot.say("```Local time : {} \n\n   {}     : {}```"
                           .format(local_time, timezone_code, converted_time))

    @commands.command()
    @asyncio.coroutine
    def seen(self, *target_users: str):
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
                yield from self.bot.say("{} could not be found..."
                                   .format(target_user))
                return

            for found_user in found_users:
                yield from self.bot.say("```\n"
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

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def setup(bot):
    """Called when cog is loaded via load_extension()."""
    bot.add_cog(Chat(bot))
