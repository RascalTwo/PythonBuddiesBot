"""Game cog."""
import random
from discord.ext import commands


tictactoe_games = {}
pokemon_games = []

class Game:
    """Game cog."""

    def __init__(self, bot):
        """Initalization function."""
        self.bot = bot
        self.temp_output = {}

    def pokemon_games(self):
        return pokemon_games

    @commands.command(pass_context=True)
    async def tictactoe(self, ctx):
        """Play tic-tac-toe without spamming messages."""
        output = await self.bot.say("Enter the message `CONSOLE:`")
        self.temp_output[ctx.message.author.id] = output

    async def receive_message(self, message):
        """Called whenever any player sends a message."""
        if message.author.id == self.bot.user.id:
            return
        if message.content == "CONSOLE:":
            if message.author.id in tictactoe_games:
                tictactoe_games[message.author.id] = TicTacToe(self.bot, self.temp_output[message.author.id])
                await tictactoe_games[message.author.id].redraw()
                del self.temp_output[message.author.id]
            my_pokemon_game = [pokemon_game for pokemon_game in pokemon_games if pokemon_game.has_user(message.author.id)]
            if my_pokemon_game != []:
                my_pokemon_game = my_pokemon_game[0]
                index = pokemon_games.index(my_pokemon_game)
                player_pos = 0 if my_pokemon_game.players[0].trainer.user_id == message.author.id else 1
                self_trainer = my_pokemon_game.players[player_pos].console_message = message
                pokemon_games[index] = my_pokemon_game
                await my_pokemon_game.redraw("Console accepted")

    @commands.group(pass_context=True)
    async def pokemon(self, ctx):
        """Base command for playing pokemon

        list, create, and join

        """
        if ctx.invoked_subcommand is None:
            await self.bot.say("list, create, join")

    @pokemon.command()
    async def list(self):
        message = "```\n"
        for game in pokemon_games:
            if len(game.players) != 2:
                message += game.players[0]["trainer"].trainer_id + "\n"
        message += "```"
        await self.bot.say(message)

    @pokemon.command(pass_context=True)
    async def join(self, ctx, trainer_id: int):
        target_game = [pokemon_game for pokemon_game in pokemon_games if pokemon_game.has_trainer(trainer_id)]
        if target_game != []:
            target_game = target_game[0]
            output_message = await self.bot.say("Enter the message `CONSOLE:`")
            index = pokemon_games.index(target_game)
            pokemon_trainer_image = ctx.message.author.default_avatar_url if ctx.message.author.avatar_url is None else ctx.message.author.avatar_url
            pokemon_trainer = Pokemon_Trainer(ctx.message.author.id, pokemon_trainer_image, ctx.message.author.name, "F")
            target_game.players.append(Pokemon_Player(pokemon_trainer, output_message, None))
            pokemon_games[index] = target_game
            await target_game.redraw("Joined pokemon game")

    @pokemon.command(pass_context=True)
    async def create(self, ctx):
        pokemon_game = Pokemon_Game(self.bot)
        output_message = await self.bot.say("Enter the message `CONSOLE: ` - space included.")
        pokemon_trainer_image = ctx.message.author.default_avatar_url if ctx.message.author.avatar_url is None else ctx.message.author.avatar_url
        pokemon_trainer = Pokemon_Trainer(ctx.message.author.id, pokemon_trainer_image, ctx.message.author.name, "M")
        pokemon_game.players.append(Pokemon_Player(pokemon_trainer, output_message, None))
        pokemon_games.append(pokemon_game)
        await pokemon_game.redraw("Pokemon game created")

    async def edit_message(self, before, after):
        if after.author.id == self.bot.user.id:
            return

        if after.author.id in tictactoe_games:
            tictactoe_games[after.author.id].receive_command(after.content.split("CONSOLE: ")[1])
            await tictactoe_games[after.author.id].redraw()

class Pokemon_Game(object):
    def __init__(self, bot):
        self.bot = bot
        self.players = []
        self.current_turn = 0

    async def redraw(self, message):
        for player in self.players:
            await player.redraw(self.bot, message)

    @property
    def user_ids(self):
        return [player.trainer.user_id for player in self.players]

    @property
    def trainer_ids(self):
        return [player.trainer.trainer_id for player in self.players]

    def get_trainer_by_user_id(self, user_id):
        for player in self.players:
            if player.user_id == user_id:
                return player
        return None

    def has_user(self, id):
        return id in self.user_ids

    def has_trainer(self, id):
        return id in self.trainer_ids

    def logic(self, player, message):
        print("Goot")

class Pokemon_Player(object):
    def __init__(self, trainer, output_message, console_message):
        self.trainer = trainer
        self.output_message = output_message
        self.console_message = console_message

    async def redraw(self, bot, message):
        await bot.edit_message(self.output_message, message)

class Pokemon_Trainer(object):
    def __init__(self, user_id, image, name, gender):
        self.user_id = user_id
        self.trainer_id = random.randint(1000, 9999)
        self.image = image
        self.name = name
        self.gender = gender
        self.items = []
        self.pokemon = []

class Pokemon(object):
    def __init__(image, name, gender, description, base_stats, stat_rate):
        self.image = image
        self.name = name
        self.gender = gender
        self.description = description
        self.base_stats = base_stats
        self.stat_rate = stat_rate
        self.level = 1
        self.current_stats = None
        self.skills = []

    def update_stats(self):
        self.current_stats["hp"] = self.base_stats["hp"] + self.stat_rate["hp"]
        self.current_stats["pp"] = self.base_stats["pp"] + self.stat_rate["pp"]
        self.current_stats["acc"] = self.base_stats["acc"] + self.stat_rate["acc"]

class Skill(object):
    def __init__(self, icon, description, stat_change, pp_cost):
        self.icon = icon
        self.description = description
        self.stat_change = stat_change
        self.pp_cost = pp_cost

    def use(self, pokemon_target):
        pokemon_target.current_stats["hp"] += self.stat_change["hp"]
        pokemon_target.current_stats["pp"] += self.stat_change["pp"]
        pokemon_target.current_stats["acc"] += self.stat_change["acc"]

class Item(object):
    def __init__(self, icon, name, description, stat_change):
        self.icon = icon
        self.description = description
        self.stat_change = stat_change

    def use(self, pokemon_target):
        pokemon_target.current_stats["hp"] += self.stat_change["hp"]
        pokemon_target.current_stats["pp"] += self.stat_change["pp"]
        pokemon_target.current_stats["acc"] += self.stat_change["acc"]

class TicTacToe(object):
    def __init__(self, bot, output_message):
        self.bot = bot
        self.output_message = output_message
        self.board = [
                      [" ", " ", " "],
                      [" ", " ", " "],
                      [" ", " ", " "]
                     ]
        self.status_message = "Enter where you want to place your O!"

    async def redraw(self):
        await self.bot.edit_message(self.output_message,
                                    self.board_string() + "\n" + self.status_message)

    def board_string(self):
        board_string = ("```\n"
                        "┌─┬─┬─┐\n"
                        "├{}┼{}┼{}┤\n"
                        "├{}┼{}┼{}┤\n"
                        "├{}┼{}┼{}┤\n"
                        "└─┴─┴─┘\n"
                        "```"
                        .format(self.board[0][0], self.board[0][1], self.board[0][2],
                                self.board[1][0], self.board[1][1], self.board[1][2],
                                self.board[2][0], self.board[2][1], self.board[2][2]))

        return board_string

    def receive_command(self, string):
        if not string.split(" ")[0].isdecimal() or not string.split(" ")[1].isdecimal():
            self.status_message = "Must have x and y as int"
            return

        x = int(string.split(" ")[0])
        y = int(string.split(" ")[1])

        if (x <= 0 or x >= 4) or (y <= 0 or y >= 4):
            self.status_message = "Must be between 1 and 3"
            return

        if self.board[x-1][y-1] != " ":
            self.status_message = "That spot is filled"
            return

        self.board[x-1][y-1] = "O"

        if self.check_win():
            self.status_message = "You Win!"
            return
        elif self.check_lose():
            self.status_message = "You Lost!"
            return
        elif self.game_over():
            self.status_message = "Draw!"
            return
        else:
            self.bot_move()
            return

    def bot_move(self):
        for _ in range(10):
            x = random.randint(0, 2)
            y = random.randint(0, 2)
            if self.board[x][y] != " ":
                continue
            self.board[x][y] = "X"
            return
        for x in range(3):
            for y in range(3):
                if self.board[x][y] == " ":
                    self.board[x][y] = "X"
                    return
        self.status_message = "Bot has moved, your turn now."

    def check_win(self):
        board = self.board
        return ((board[0][0] != " " and board[0][0] != "X" and board[0][0] == board[0][1] and board[0][1] == board[0][2]) or
                (board[1][0] != " " and board[1][0] != "X" and board[1][0] == board[1][1] and board[1][1] == board[1][2]) or
                (board[2][0] != " " and board[2][0] != "X" and board[2][0] == board[2][1] and board[2][1] == board[2][2]) or
                (board[0][0] != " " and board[0][0] != "X" and board[0][0] == board[1][0] and board[1][0] == board[2][0]) or
                (board[0][1] != " " and board[0][1] != "X" and board[0][1] == board[1][1] and board[1][1] == board[2][1]) or
                (board[0][2] != " " and board[0][2] != "X" and board[0][2] == board[1][2] and board[1][2] == board[2][2]) or
                (board[0][0] != " " and board[0][0] != "X" and board[0][0] == board[1][1] and board[1][1] == board[2][2]) or
                (board[2][2] != " " and board[2][2] != "X" and board[2][2] == board[1][1] and board[1][1] == board[0][0]))

    def check_lose(self):
        board = self.board
        return ((board[0][0] != " " and board[0][0] != "O" and board[0][0] == board[0][1] and board[0][1] == board[0][2]) or
                (board[1][0] != " " and board[1][0] != "O" and board[1][0] == board[1][1] and board[1][1] == board[1][2]) or
                (board[2][0] != " " and board[2][0] != "O" and board[2][0] == board[2][1] and board[2][1] == board[2][2]) or
                (board[0][0] != " " and board[0][0] != "O" and board[0][0] == board[1][0] and board[1][0] == board[2][0]) or
                (board[0][1] != " " and board[0][1] != "O" and board[0][1] == board[1][1] and board[1][1] == board[2][1]) or
                (board[0][2] != " " and board[0][2] != "O" and board[0][2] == board[1][2] and board[1][2] == board[2][2]) or
                (board[0][0] != " " and board[0][0] != "O" and board[0][0] == board[1][1] and board[1][1] == board[2][2]) or
                (board[2][2] != " " and board[2][2] != "O" and board[2][2] == board[1][1] and board[1][1] == board[0][0]))

    def game_over(self):
        for row in self.board:
            for col in row:
                if col == " ":
                    return False

        return True


def setup(bot):
    """Called when cog is loaded via load_extension()."""
    game = Game(bot)
    bot.add_listener(game.receive_message, "on_message")
    bot.add_listener(game.edit_message, "on_message_edit")
    bot.add_cog(game)
