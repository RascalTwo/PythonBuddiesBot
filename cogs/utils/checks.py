from discord.ext import commands
import config
import discord.utils
import json


def is_owner_check(message):
    """This is the bot owners ID, it is found from the config.py file"""
    return message.author.id == config.owner


def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message))
