"""Game cog."""
import random
from discord.ext import commands


checker_games = {}

class Game:
    """Game cog."""

    def __init__(self, bot):
        """Initalization function."""
        self.bot = bot
        self.temp_output = {}

    @commands.group(pass_context=True)
    async def checkers(self, ctx):
        """Base command for playing pokemon

        list, create, and join

        """
        if ctx.invoked_subcommand is None:
            await self.bot.say("list, create, join")

    @checkers.command()
    async def list(self):
        message = "```\n"
        for game_id in checker_games:
            if len(checker_games[game_id].players) != 2:
                message += "{}\n".format(game_id)
        message += "```"
        await self.bot.say(message)

    @checkers.command(pass_context=True)
    async def join(self, ctx, game_id: int):
        checker_game = checker_games[game_id]
        checker_game.players.append(Checker_Player(ctx.message.author.id, ["B", "G"]))
        checker_game.status_message = "Player 2 joined, enter the `CONSOLE:` message."
        await checker_game.redraw()


    @checkers.command(pass_context=True)
    async def create(self, ctx):
        output_message = await self.bot.say("Enter the message `CONSOLE:`")
        checker_game = Checker_Game(self.bot, output_message)
        checker_game.players.append(Checker_Player(ctx.message.author.id, ["W", "S"]))
        checker_games[checker_game.id] = checker_game
        await checker_game.redraw()

    async def receive_message(self, message):
        """Called whenever any player sends a message."""
        if message.author.id == self.bot.user.id:
            return
        if message.content == "CONSOLE:":
            try:
                checker_game = [checker_game for checker_game in checker_games.values() if any(message.author.id == checker_player.id for checker_player in checker_game.players)][0]
            except Exception as e:
                await self.bot.send_message(message.channel, "You haven't joined a checkers game!")
                return
            #Changed to allow player to play against self.
            checker_player = [checker_player for checker_player in checker_game.players if checker_player.id == message.author.id][-1]
            checker_player.message = message
            if len(checker_game.players) != 2:
                checker_game.status_message = "Waiting for 2nd player..."
            else:
                checker_game.status_message = "Player 1 - Enter your `from` and `to` coordnates."
            for player in checker_game.players:
                print("{}-{}-{}".format(player.id, player.message, player.chars))
            checker_games[checker_game.id] = checker_game
            await checker_game.redraw()

    async def edit_message(self, before, after):
        if after.author.id == self.bot.user.id:
            return
        try:
            checker_game = [checker_game for checker_game in checker_games.values() if any(after.author.id == checker_player.id for checker_player in checker_game.players)][0]
        except Exception as e:
            return
        checker_game.receive_command(checker_game.player_from_id(after.author.id), after.content.split("CONSOLE:")[1].strip())
        await checker_game.redraw()

    def checker_games(self):
        return checker_games


class Checker_Game(object):
    def __init__(self, bot, output_message):
        self.id = random.randint(1000, 9999)
        self.bot = bot
        self.players = []
        self.current_turn = 0
        self.board = [
                      [" ", "W", " ", "W", " ", "W", " ", "W"],
                      ["W", " ", "W", " ", "W", " ", "W", " "],
                      [" ", "W", " ", "W", " ", "W", " ", "W"],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      ["B", " ", "B", " ", "B", " ", "B", " "],
                      [" ", "B", " ", "B", " ", "B", " ", "B"],
                      ["B", " ", "B", " ", "B", " ", "B", " "],
                     ]
        self.status_message = "Created game ID {}, Enter the message `CONSOLE:`".format(self.id)
        self.output_message = output_message

    async def redraw(self):
        await self.bot.edit_message(self.output_message,
                                    self.board_string() + "\n" + self.status_message)

    def board_string(self):
        board_string = "```\n   1 2 3 4 5 6 7 8\n  ┌─┬─┬─┬─┬─┬─┬─┬─┐\n"
        for i in range(len(self.board)):
            board_string += str(i + 1) + " │" + "│".join(self.board[i]) + "│\n"
            if i != 7:
                board_string += "  ├─┼─┼─┼─┼─┼─┼─┼─┤\n"
            else:
                board_string += "  └─┴─┴─┴─┴─┴─┴─┴─┘\n```"
        return board_string

    def player_from_id(self, id):
        for player in self.players:
            if player.id == id:
                return player
        return None

    def receive_command(self, sender, command):
        if len(self.players) != 2:
            self.status_message = "Waiting for 2nd player..."
            return

#        if self.players.index(sender) != self.current_turn:
#            self.status_message = "It's not your turn Player {}!".format(self.players.index(sender))
#            return

        if not command.split(" ")[0].isdecimal() or not command.split(" ")[1].isdecimal():
            self.status_message = "Must have `from` and `to` as int"
            return

        from_cord = [int(cord) for cord in command.split(" ")[0]][::-1]
        to_cord = [int(cord) for cord in command.split(" ")[1]][::-1]
        #
#        print("From:{}-{}\n{}".format(from_cord, self._get_board_piece(from_cord), self.board[from_cord[0]-1]))
#        print("To:{}-{}\n{}".format(to_cord, self._get_board_piece(to_cord), self.board[to_cord[0]-1]))
        #
        for cord in [from_cord, to_cord]:
            if not self._cord_on_board(cord):
                self.status_message = "Must be between 1 and 8"
                return

        if not any(self._get_board_piece(from_cord) == char for char in sender.chars):
            self.status_message = "Your from coordnate is not one of your pieces."
            return

        if self._get_board_piece(to_cord) != " ":
#            trying = [True, to_cord]
#            while trying:
#                if to_cord[0] - 2 > 0 and to_cord[0]
            self.status_message = "That spot is filled"
            return

        self._move_board_piece(from_cord, to_cord)

        self.current_turn = 0 if self.current_turn == 1 else 1

    def _cord_on_board(self, cord):
        return (cord[0] > 0 or cord[0] < 9) and (cord[1] > 0 or cord[1] < 9)

    def _get_board_piece(self, cord):
        return self.board[cord[0]-1][cord[1]-1]

    def _move_board_piece(self, from_cord, to_cord):
        self.board[to_cord[0]-1][to_cord[1]-1] = self._get_board_piece(from_cord)
        self.board[from_cord[0]-1][from_cord[1]-1] = " "


class Checker_Player(object):
    def __init__(self, id, chars):
        self.id = id
        self.message = None
        self.chars = chars
        self.pieces_lost = 0


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


def setup(bot):
    """Called when cog is loaded via load_extension()."""
    game = Game(bot)
    bot.add_listener(game.receive_message, "on_message")
    bot.add_listener(game.edit_message, "on_message_edit")
    bot.add_cog(game)
