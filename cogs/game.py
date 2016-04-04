"""Game cog."""
import random
from discord.ext import commands

games = {}

class Game:
    """Game cog."""

    def __init__(self, bot):
        """Initalization function."""
        self.bot = bot
        self.temp_output = {}

    @commands.command(pass_context=True)
    async def tictactoe(self, ctx):
        output = await self.bot.say("Enter the message `CONSOLE:`")
        print(type(ctx.message.author.id))
        print(ctx.message.author.id)
        self.temp_output[ctx.message.author.id] = output

    async def receive_message(self, message):
        """Called whenever any player sends a message."""
        if message.author.id == self.bot.user.id:
            return
        if message.content == "CONSOLE:":
            if message.author.id not in self.temp_output:
                await self.bot.say("You need to start a game before creating your CONSOLE message.")
                return
            games[message.author.id] = TicTacToe(self.bot, self.temp_output[message.author.id])
            await games[message.author.id].redraw()
            del self.temp_output[message.author.id]


    async def edit_message(self, before, after):
        if after.author.id == self.bot.user.id:
            return

        if after.author.id in games:
            games[after.author.id].receive_command(after.content.split("CONSOLE: ")[1])
            await games[after.author.id].redraw()


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
