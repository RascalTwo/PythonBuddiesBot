"""Checks utility file.

Contains checks to be used as decorators for commands.

"""
from discord.ext import commands
import config


def is_owner_check(message):
    """Return if the message author equals the bot owner."""
    return message.author.id == config.owner


def is_owner():
    """Decorator method to return if the message executor is the bot owner."""
    return commands.check(lambda ctx: is_owner_check(ctx.message))
