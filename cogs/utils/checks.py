from discord.ext import commands
import discord.utils


def is_owner_check(message):
    """This is the bot owners ID, this can be changed to suit needs per environment."""
    return message.author.id == '66231907616038912' # Set to OnyxChills


def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message))