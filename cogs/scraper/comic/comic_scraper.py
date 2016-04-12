"""Comic scraper cog.

Contains comic, comic random, and comic latest commands - the latter
two choose a random command from sub-group-commands of comic to execute.

"""
import random
from discord.ext import commands
from ..scraper_utils import GeneralScraper

class ComicScraper(GeneralScraper):
    """Main base comic cog.

    Extends GeneralScraper.
    Contains the comic, comic latest, and comic random commands.

    """

    def __init__(self, bot):
        """Initalization method."""
        super().__init__()
        self.bot = bot
        self.current_comic = 0

    @commands.group(pass_context=True)
    async def comic(self, ctx):
        """Main comic command."""
        if ctx.invoked_subcommand is None:
            await ctx.bot.pm_help(ctx)

    @comic.command(name="random", pass_context=True)
    async def comic_random(self, ctx):
        """Return random comic from a random comic website."""
        random_methods = get_all_subcommands(ComicScraper.comic, "random")
        await random.choice(random_methods).invoke(ctx)

    @comic.command(name="latest", pass_context=True)
    async def comic_latest(self, ctx):
        """Return the latest comic from the next comic website."""
        latest_methods = get_all_subcommands(ComicScraper.comic, "latest")
        await latest_methods[self.current_comic].invoke(ctx)
        self.current_comic = self.current_comic + 1 if self.current_comic != len(latest_methods)-1 else 0


def get_all_subcommands(group, must_contain=None,):
    """Return all subcommands of supplied group command.

    Keyword Arguments:
    group -- Group command to get subcommands of.
    must_contains -- String that subcommands must
                     contain in their command name.
                     (default None)

    Returns:
    list - Subcommands found.

    Note: Will only search one subsequent layer of group commands.
    """
    commands_found = []
    for comic_group_command in group.commands.keys():
        if not isinstance(group.commands[comic_group_command], commands.Group):
            continue
        current_comic_subcommands = group.commands[comic_group_command].commands
        for comic_subcommand in current_comic_subcommands:
            if must_contain is None or must_contain in current_comic_subcommands[comic_subcommand].name:
                commands_found.append(current_comic_subcommands[comic_subcommand])
    return commands_found


def setup(bot):
    """Called when cog is loaded via load_extension()."""
    bot.add_cog(ComicScraper(bot))
