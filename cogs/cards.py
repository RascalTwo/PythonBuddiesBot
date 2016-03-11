"""Cards cog.

Will contain many card playable card games.

"""
from discord.ext import commands
import random

playing_users = {}


def generate_deck(value_rules, jokers=0, joker_value=0):
    """Generate a list of unique cards.

    Keyword Arguments:
    jokers -- Number of Jokers to add to Deck. (default 0)
    joker_value -- Value for each Joker generated. (default 0)
    value_rules -- Value(int)-Rank(str) dictionary for each Card generated. (example {1: "Ace"})

    Returns:
    list -- List of Cards, each being unique asside from possible Jokers.
    """
    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
    deck = [Card(value_rules, value, suit) for value in value_rules for suit in suits]
    deck.extend([Card({joker_value: "Joker"}, joker_value, "") for _ in range(jokers)])
    return deck


class Card:
    """A playing Card."""

    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]

    def __init__(self, value_rules, value, suit):
        """Create a new Card with the supplied `value` and `suit`, getting rank name from `value_rules`.

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
        return self.__class__ == other.__class__ and self.rank == other.rank and self.suit == other.suit and self.value == other.value

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
        value_rules -- Value(int)-Rank(str) dictionary for each Card generated. (example {1: "Ace"})

        Returns:
        card - Randomly chosen card from `value_rules`.

        """
        return Card(value_rules, random.choice(list(value_rules.keys())), random.choice(["Clubs", "Diamonds", "Hearts", "Spades"]))


class HiLo_Game:
    """HiLo Game instance."""

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
    responces = {"guess": ["higher", "lower"], "choose": ["double", "pass"]}

    def __init__(self, user, bet_amount):
        """Create a new HiLo game with the supplied player.

        Keyword Arguments:
        user -- User to play HiLo.
        bet_amount -- Amount of money bet.

        """
        self.user = user
        self.bet_amount = int(bet_amount)
        self.stage = "guess"
        self.card_hidden = None
        self.card_visible = None
        self._new_cards()

    def _new_cards(self):
        self.card_hidden = Card.random(self.value_rules)
        self.card_visible = Card.random(self.value_rules)
        while self.card_hidden == self.card_visible:
            self.card_hidden = Card.random(self.value_rules)

    def get_message(self, message, params=None):
        """Return a Message.

        Keyword Arguments:
        message -- Message to get.

        Returns:
        str -- Message with variables filled in.

        """
        if message == "game_start":
            return "So, do you think the face-down card is *higher* or *lower* then the **{}**?".format(self.card_visible)
        elif message == "double_or_pass":
            return "Do you wish to go for *double* or nothing, or will you take your winnings and *pass*?"
        elif message == "user_won":
            return "You Won $**{}**!\nDo you wish to go for *double* or nothing, or will you take your winnings and *pass*?".format(self.bet_amount * 2)
        elif message == "user_lose":
            return "You Lost $**{}**!\nBetter luck next time!".format(self.bet_amount)
        elif message == "guess_result":
            return "The **{}** {}{} then the **{}**".format(self.card_hidden, "is " if params[0] else "is not ", params[1], self.card_visible)
        elif message == "game_won":
            return "Thanks for playing!\n$**{}** has been added to your account!".format(self.bet_amount * 2)

    def guess(self, guess):
        """Guess weather the hidden card is higher or lower than the hidden card.

        Returns:
        bool -- True if the user was correct, False otherwise.

        """
        if guess.lower() == "higher"and self.card_hidden.value > self.card_visible.value:
            self.stage = "choose"
            return True
        elif guess.lower() == "lower" and self.card_hidden.value < self.card_visible.value:
            self.stage = "choose"
            return True
        else:
            return False

    def choose(self, choice):
        """Choose to either go for double or nothing, or to pass and take your winnings.

        Keyword Arguments:
        choice -- User choice, either being `double` or `pass`.

        Returns:
        bool -- True if the game is continuing, False otherwise

        """
        if choice.lower() == "double":
            if False:  # User doesn't have enough money to go double or nothing
                return False
            self.bet_amount *= 2
            self._new_cards()
            self.stage = "guess"
            return True
        elif choice.lower() == "pass":
            self.stage = "won"
            return False


class Cards:
    """Card cog."""

    def __init__(self, bot):
        """Initalization function."""
        self.bot = bot

    @commands.command(pass_context=True)
    async def game(self, ctx):
        """Base command for playing card games.

        Keyword arguments:
        ctx -- Command context.

        """
        arguments = ctx.message.content.split(" ")
        game_name = arguments[1]
        if game_name.lower() == "hilo":
            if len(arguments) != 3:
                await self.bot.say("Correct command: 'game hilo bet_amount'\nExample: 'game hilo 10'")
                return
            if not arguments[2].isdecimal():
                await self.bot.say("Bet amount needs to be a number.")
                return
            if False:  # TODO: Replace with not enough money economy check.
                await self.bot.say("You don't have ${}!".format(arguments[2]))
                return
            hilo_game_instance = HiLo_Game(ctx.message.author, arguments[2])
            await self.bot.say(hilo_game_instance.get_message("game_start"))
            playing_users[ctx.message.author.id] = hilo_game_instance
#                   FIX: Above error messages are only placeholders at the moment.

    async def receive_message(self, message):
        """Called whenever any player sends a message."""
        if message.author.id == self.bot.user.id or message.author.id not in playing_users:
            return
        game = playing_users[message.author.id]
        if isinstance(game, HiLo_Game):
            if message.content.lower() not in game.responces[game.stage]:
                return
            if game.stage == "guess":
                won = game.guess(message.content.lower())
                responce_message = game.get_message("guess_result", [won, message.content.lower()])
                if won:
                    responce_message += "\n" + game.get_message("user_won")
                else:
                    responce_message += "\n" + game.get_message("user_lose")
#                   TODO: Remove game.bet_amount from user account.
                    del playing_users[message.author.id]
                await self.bot.send_message(message.channel, responce_message)
            elif game.stage == "choose":
                double = game.choose(message.content.lower())
                if double:
                    responce_message = game.get_message("game_start")
                else:
                    responce_message = game.get_message("game_won")
#                   TODO: Add game.bet_amount * 2 to user account.
                    del playing_users[message.author.id]
                await self.bot.send_message(message.channel, responce_message)


def setup(bot):
    """Called when cog is loaded via load_extension()."""
    cards = Cards(bot)
    bot.add_listener(cards.receive_message, "on_message")
    bot.add_cog(cards)
