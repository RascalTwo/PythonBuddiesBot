"""Cards cog.

Will contain many card playable card games.

"""
import random
from discord.ext import commands
from .utils import fileIO
import asyncio
playing_users = {}


class Cards:
    """Card cog."""

    def __init__(self, bot):
        """Initalization function."""
        self.bot = bot

    @commands.command(pass_context=True)
    @asyncio.coroutine
    def balance(self, ctx):
        """Return the balance of executing user."""
        yield from self.bot.say("Current Balance: $**{}**"
                           .format(Economy.get_user_balance(ctx.message.author.id)))

    @commands.group(pass_context=True)
    @asyncio.coroutine
    def game(self, ctx):
        """Base command for playing card games.

        Playable games:

        HiLo - game hilo bet_amount

        """
        if ctx.invoked_subcommand is None:
            yield from self.bot.say("Try one of these games:\n"
                               "HiLo - game hilo bet_amount")

    @game.command(pass_context=True)
    @asyncio.coroutine
    def hilo(self, ctx):
        """Start a game of HiLo.

        HiLo is a game in which two unique cards are randomly generated. You
        are then told the value of one of these cards, and must guess if the
        other value of the other card is either higher, or lower then the value
        of the first card.

        If you are correct, you win and may either take your money, or go for
        double or nothing!

        Values from least to greatest:
            Ace, 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King

        Command: game hilo bet_amount
        Example: game hilo 10

        """
        arguments = ctx.message.content.lower().split(" ")
        if len(arguments) != 3:
            yield from self.bot.say("```Command: game hilo bet_amount\n"
                               "Example: game hilo 10```")
            return
        if not arguments[2].isdecimal():
            yield from self.bot.say("```Bet amount needs to be a number.```")
            return
        if Economy.get_user_balance(ctx.message.author.id) < int(arguments[2]):
            yield from self.bot.say("`You don't have $**{}**!`"
                               .format(arguments[2]))
            return
        hilo_game_instance = HiLo_Game(ctx.message.author, arguments[2])
        Economy.change_user_balance(ctx.message.author.id,
                                    int(arguments[2]) * -1)
        yield from self.bot.say("Current Balance: $**{}**"
                           .format(Economy.get_user_balance(ctx.message.author.id)))
        yield from self.bot.say(hilo_game_instance.logic())
        playing_users[ctx.message.author.id] = hilo_game_instance

    @asyncio.coroutine
    def receive_message(self, message):
        """Called whenever any player sends a message."""
        if (message.author.id == self.bot.user.id or
                message.author.id not in playing_users):
            return
        game = playing_users[message.author.id]
        if isinstance(game, HiLo_Game):
            response = game.logic(message)
            if response is not None:
                yield from self.bot.send_message(message.channel, response)


class Card(object):
    """A playing Card."""

    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]

    def __init__(self, value_rules, value, suit):
        """Create a new Card with the supplied `value` and `suit`.

        Keyword Arguments:
        value_rules -- Value(int)-Rank(str) dictionary (example {1: "Ace"})
        value -- Value of card, determines rank name from `value_rules`.
        suit -- Suite of the Card [Clubs, Diamonds, Hearts, Spades]

        """
        self.value_rules = value_rules
        self.value = value
        self.suit = suit

    def __eq__(self, other):
        """Allow Card to be compared to other Card with the == operator.

        Keyword Arguments:
        other -- Card to see if this card is equal to.

        Returns:
        bool -- True if this Card and 'other' Card are equal, False otherwise.

        """
        return (self.__class__ == other.__class__ and
                self.rank == other.rank and
                self.suit == other.suit and
                self.value == other.value)

    @property
    def rank(self):
        """Return Rank of Card."""
        return self.value_rules[self.value]

    def __str__(self):
        """Return string representation of Card."""
        if self.suit == "":
            return self.rank
        return "{} of {}".format(self.rank, self.suit)

    def __repr__(self):
        """Return data representation of Card."""
        return "Card({},{},{})".format(self.rank, self.suit, self.value)

    @staticmethod
    def random(value_rules):
        """Return random Card of one of the `value_rules`.

        Keyword Arguments:
        value_rules -- Value(int)-Rank(str) dictionary for each Card generated.
                       (example {1: "Ace"})

        Returns:
        card - Randomly chosen card from `value_rules`.

        """
        return Card(value_rules, random.choice(list(value_rules.keys())),
                    random.choice(["Clubs", "Diamonds", "Hearts", "Spades"]))

    @staticmethod
    def generate_deck(value_rules, jokers=0, joker_value=0):
        """Generate a list of unique cards.

        Keyword Arguments:
        jokers -- Number of Jokers to add to Deck. (default 0)
        joker_value -- Value for each Joker generated. (default 0)
        value_rules -- Value(int)-Rank(str) dictionary for each Card generated.
                       (example {1: "Ace"})

        Returns:
        list -- List of Cards, each being unique asside from possible Jokers.

        """
        suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
        deck = [Card(value_rules, value, suit)
                for value in value_rules for suit in suits]
        deck.extend([Card({joker_value: "Joker"}, joker_value, "")
                     for _ in range(jokers)])
        return deck


class Economy(object):
    """Economy utility class."""

    @staticmethod
    def get_user_balance(user_id):
        """Get the balance of a user by the provided user_id.

        Keyword Arguments:
        user_id -- ID of the user to get the balance of.

        Returns:
        int -- balance of the provided user_id.

        """
        data = fileIO.readFile("data/economy.json")
        if user_id in data:
            return data[user_id]
        Economy.set_user_balance(user_id, 100)
        return 100

    @staticmethod
    def set_user_balance(user_id, balance):
        """Set the balance of a user to the provided balance.

        Keyword Arguments:
        user_id -- ID of the user to set the balance of.
        balance -- Balance to set the balance of the user to.

        Returns:
        bool -- True if the setting of the users balance was
                successful, otherwise False.

        """
        data = fileIO.readFile("data/economy.json")

        if balance > data["minimum_balance"]:
            data[user_id] = balance
        else:
            data[user_id] = data["minimum_balance"]

        return fileIO.writeFile("data/economy.json", data)

    @staticmethod
    def change_user_balance(user_id, amount):
        """Change the balance of a user by the provided balance.

        Keyword Arguments:
        user_id -- ID of the user to change the balance of.
        amount -- Amount to change the balance of the user
                  by - can be a negative number.

        Returns:
        bool -- True if the changing of the users balance was
                successful, otherwise False.

        """
        return Economy.set_user_balance(user_id,
                                        Economy.get_user_balance(user_id) + amount)


class HiLo_Game(object):
    """HiLo Game."""

    value_rules = {
        1: "Ace",
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7",
        8: "8",
        9: "9",
        10: "10",
        11: "Jack",
        12: "Queen",
        13: "King"
    }
    responses = {"start": [None],
                 "guess": ["higher", "lower"],
                 "choose": ["double", "pass"]}

    def __init__(self, user, bet_amount):
        """Create a new HiLo game with the supplied player.

        Keyword Arguments:
        user -- User to play HiLo.
        bet_amount -- Amount of money bet.

        """
        self.user = user
        self.bet_amount = int(bet_amount)
        self.stage = "start"
        self.card_hidden = None
        self.card_visible = None
        self._new_cards()

    def _new_cards(self):
        self.card_hidden = Card.random(self.value_rules)
        self.card_visible = Card.random(self.value_rules)
        while self.card_hidden == self.card_visible:
            self.card_hidden = Card.random(self.value_rules)

    def logic(self, message=None):
        """Contain all Game execution logic.

        Keyword Arguments:
        message -- Message from the user. (default None)

        Returns:
        str or None -- Returns a message to say into the chat, if any.

        """
        if message is not None:
            message.content = message.content.lower()
            if message.content not in self.responses[self.stage]:
                return
        else:
            if message not in self.responses[self.stage]:
                return

        if self.stage == "start":
            self.stage = "guess"
            return ("So, do you think the face-down card is `higher` or "
                    "`lower` then the **{}**?".format(self.card_visible))

        if self.stage == "guess":
            response = ""
            if ((message.content == "higher" and
                 self.card_hidden.value > self.card_visible.value) or
                    (message.content == "lower" and
                     self.card_hidden.value < self.card_visible.value)):
                response += ("You Won $**{}**!\nDo you wish to go for "
                             "`double` or nothing, or will you take your "
                             "winnings and `pass`?"
                             .format(self.bet_amount * 2))
                is_or_is_not = "is"
                self.stage = "choose"
            else:
                response += ("You Lost $**{}**, leaving you with {}!\n"
                             "Better luck next time!"
                             .format(self.bet_amount,
                                     Economy.get_user_balance(self.user.id)))
                is_or_is_not = "is not"
                del playing_users[message.author.id]
            response = ("The **{}** {} {} then the **{}**\n"
                        .format(self.card_hidden,
                                is_or_is_not,
                                message.content,
                                self.card_visible)) + response
            return response

        elif self.stage == "choose":
            response = ""
            if message.content == "double":
                if Economy.get_user_balance(self.user.id) >= self.bet_amount * 2:
                    self._new_cards()
                    response += ("So, do you think the face-down card is "
                                 "`higher` or `lower` then the **{}**?"
                                 .format(self.card_visible))
                    self.bet_amount *= 2
                    self.stage = "guess"
                else:
                    response += ("You don't have ${} to bet, passing instead\n"
                                 .format(self.bet_amount * 2))
                    message.content = "pass"
            if message.content == "pass":
                response += ("Thanks for playing!\n$**{}** has been added to "
                             "your account, bringing your balance to $**{}**!"
                             .format(self.bet_amount * 2,
                                     self.bet_amount * 2 + Economy.get_user_balance(self.user.id)))
                Economy.change_user_balance(self.user.id, self.bet_amount * 2)
                del playing_users[message.author.id]
            return response


def setup(bot):
    """Called when cog is loaded via load_extension()."""
    if fileIO.readFile("data/economy.json") is False:
        fileIO.writeFile("data/economy.json", {"minimum_balance": 100})

    cards = Cards(bot)
    bot.add_listener(cards.receive_message, "on_message")
    bot.add_cog(cards)
