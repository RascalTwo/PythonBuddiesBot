"""A bird."""
import random
from discord.ext import commands

class MUD(object):
    """MUD game."""

    def __init__(self, bot):
        self.bot = bot
        self.players
        self.world = World("Totally Not Evennia")
        coast_line = Location(self.world.generate_id(), "coast line")
        coast_line.messages["on_look"] = """To the east, you see an old hanging bridge."""

    @commands.group(pass_context=True):
    async def mud(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.pm_help(ctx)

    @mud.command(pass_context=True)
    async def join(self, ctx):
        player = Player(ctx.message.author.id)


    @commands.listen("on_message")
    async receive_message(self, message):
        if message.author.id == self.bot.user.id:
            return
        await self.bot.send_message(message.channel, "Echo - {}".format(message))


class DefaultEvents(object):
    @staticmethod
    def on_enter(player, location):
        if location.messages["on_enter"] is not None:
            player.send_message(location.messages["on_enter"])

    @staticmethod
    def on_exit(player, location):
        if location.messages["on_exit"] is not None:
            player.send_message(location.messages["on_exit"])

    @staticmethod
    def on_look(player, location):
        if location.messages["on_look"] is not None:
            player.send_message(location.messages["on_look"])


class PlayerContainer(object):
    def __init__(self):
        self.players = []

    def get_player_from_id(self, id):
        for player in players:
            if player.id == id:
                return player
        return None

    def get_player_from_user_id(self, user_id):
        for player in players:
            if player.user_id == user_id:
                return player
        return None

    def remove_player_by_id(self, id):
        for player in players:
            if player.id == id:
                players.remove(id):
                return True
        return False

    def remove_player_by_user_id(self, user_id):
        for player in players:
            if player.user_id == user_id:
                players.remove(player)
                return True
        return False

class World(PlayerContainer):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.locations = []

    def location_from_name(self, name):
        for location in locations:
            if location.name == name:
                return location
        return None

    def location_from_id(self, id):
        for location in locations:
            if location.id == id:
                return location
        return None

    def generate_id(self):
        new_id = random.randint(100, 999)
        if self.player_from_id(new_id) != None:
            return self.generate_id()
        for player in self.players:
            for item in player.inventory:
                if item.id == new_id:
                    return self.generate_id()
        if self.location_from_id(new_id) != None:
            return self.generate_id()
        for location in self.locations:
            for enviroment_object in location.enviroment_objects:
                if enviroment_object.id == new_id:
                    return self.generate_id()
        return new_id

class Location(PlayerContainer):
    def __init__(self, id, name):
        super().__init__()
        self.id = id
        self.name = name
        self.enviroment_objects = []
        self.routes = {}
        self.messages = {
            "on_enter": None,
            "on_exit": None,
            "on_look": None
        }
        self.events = {
            "on_enter": None,
            "on_exit": None,
            "on_look": None
        }

    @property
    def route_options(self):
        return list(self.routes.keys())

class EnviromentObject(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.messages = {
            "on_look": None
        }

class Item(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Player(object):
    def __init__(self, id, user_id):
        self.id = id
        self.user_id = user_id
        self.location = None
        self.inventory = []
        self.stats = {
            "hp": 100,
            "energy": 100
        }

    def move_to_location(self, location):
        self.location.events["on_exit"](self, self.location)
        self.location.remove_player_by_id(self.id)
        self.location = location
        self.location.players.append(self)
        self.location.

def setup(bot):
    """Add cog."""
    bot.add_cog(MUD(bot))
