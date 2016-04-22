from discord.ext import commands
from .scraper.scraper_utils import GeneralScraper
import asyncio


class Trello(GeneralScraper):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        asyncio.ensure_future(self.log_users())
        self.last_actions = {}
        self.update_channel = None

    async def check_actions(self):
        first = True
        while True:
            boards = self.fetch_json("https://api.trello.com/1/organizations/pybuddies/boards")
            new_actions = []
            for board in boards:
                board_actions = self.fetch_json("https://api.trello.com/1/boards/{}/actions".format(board["id"]))
                if first:
                    self.last_actions[board["id"]] = board_actions[0]["id"]
                    continue
                if self.last_actions[board["id"]] == board_actions[0]["id"]:
                    continue
                new_board_actions = []
                for action in board_actions:
                    if action["id"] == self.last_actions[board["id"]]:
                        break
                    new_board_actions.append(action)
                new_actions.append(new_board_actions)
            message = "```\n"
            for new_board_actions in new_actions:
                message += "      Board: {}\n".format(new_board_actions[0]["data"]["board"]["name"])
                for action in new_board_actions:
                    message += "────────────\n"
                    message += "{}\n".format(action["member"]["full_name"])
                    message += "{}\n".format(action["type"])
                    message += "{}\n".format(action["card"]["name"])
                    message += "────────────\n"
            message += "```"
            if self.update_channel is not None:
                await self.bot.send_message(self.update_channel, message)
            await asyncio.sleep(60)

    @commands.group(pass_context=True)
    async def trello(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.pm_help(ctx)

    @comic.group(pass_context=True)
    async def boards(self, ctx):
        pass

    @comic.group(pass_context=True)
    async def update(self, ctx):
        await self.bot.say("Update Channel Set")
        self.update_channel = ctx.message.channel

def setup(bot):
    """Called when cog is loaded via load_extension()."""
    bot.add_cog(ComicScraper(bot))
