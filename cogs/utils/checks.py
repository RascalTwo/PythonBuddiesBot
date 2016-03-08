from discord.ext import commands
import discord.utils
import json

def is_owner_check(message):
    """This is the bot owners ID, it is found from the settings.json file"""
    settings = json.load(open("././settings.json"))
    return message.author.id == settings["owner"]


def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message))
